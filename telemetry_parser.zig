const std = @import("std");

/// Fixed-size binary packet header for embedded UAV communications
pub const PacketHeader = packed struct {
    sync_byte1: u8 = 0xAA,
    sync_byte2: u8 = 0x55,
    payload_len: u16,
};

pub const FlightTelemetryPayload = extern struct {
    timestamp_ms: u64,
    altitude_m: f32,
    pitch_deg: f32,
    roll_deg: f32,
    battery_v: f32,
};

pub const TelemetryPacket = struct {
    header: PacketHeader,
    payload: FlightTelemetryPayload,
    checksum: u16,

    pub fn calculateChecksum(bytes: []const u8) u16 {
        var sum: u16 = 0;
        for (bytes) |b| {
            sum = sum +% b;
        }
        return sum;
    }

    pub fn isValid(self: TelemetryPacket, raw_payload_bytes: []const u8) bool {
        return self.header.sync_byte1 == 0xAA and
            self.header.sync_byte2 == 0x55 and
            self.checksum == calculateChecksum(raw_payload_bytes);
    }
};

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    try stdout.print("=== Zig Low-Latency Telemetry Decoder Initialized ===\n", .{});

    const sample_payload = FlightTelemetryPayload{
        .timestamp_ms = 125430,
        .altitude_m = 120.45,
        .pitch_deg = -2.15,
        .roll_deg = 0.85,
        .battery_v = 11.42,
    };

    const payload_bytes = std.mem.asBytes(&sample_payload);
    const packet = TelemetryPacket{
        .header = .{ .payload_len = @intCast(payload_bytes.len) },
        .payload = sample_payload,
        .checksum = TelemetryPacket.calculateChecksum(payload_bytes),
    };

    try stdout.print("Decoded Packet:\n", .{});
    try stdout.print("  Timestamp: {} ms\n", .{packet.payload.timestamp_ms});
    try stdout.print("  Altitude:  {d:.2} m\n", .{packet.payload.altitude_m});
    try stdout.print("  Battery:   {d:.2} V\n", .{packet.payload.battery_v});
    try stdout.print("  Checksum:  0x{X:0>4} [Verified: {}]\n", .{
        packet.checksum,
        packet.isValid(payload_bytes),
    });
}
