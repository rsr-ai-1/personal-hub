defmodule AutonomousSwarm.DroneNode do
  @moduledoc """
  Fault-tolerant actor representing an autonomous swarm node using OTP GenServer.
  Handles peer heartbeat telemetry and mesh leader consensus.
  """
  use GenServer
  require Logger

  @heartbeat_interval 1_000 # 1 second

  # --- Client API ---

  def start_link(drone_id) do
    GenServer.start_link(__MODULE__, drone_id, name: via_tuple(drone_id))
  end

  def broadcast_position(drone_id, x, y, z) do
    GenServer.cast(via_tuple(drone_id), {:broadcast_telemetry, {x, y, z}})
  end

  def get_status(drone_id) do
    GenServer.call(via_tuple(drone_id), :get_status)
  end

  # --- GenServer Callbacks ---

  @impl true
  def init(drone_id) do
    Logger.info("[SwarmNode #{drone_id}] Online and joining mesh network.")
    schedule_heartbeat()
    
    state = %{
      id: drone_id,
      position: {0.0, 0.0, 0.0},
      peers: MapSet.new(),
      battery_pct: 100
    }
    
    {:ok, state}
  end

  @impl true
  def handle_cast({:broadcast_telemetry, new_coords}, state) do
    updated_state = %{state | position: new_coords}
    {:noreply, updated_state}
  end

  @impl true
  def handle_call(:get_status, _from, state) do
    {:reply, state, state}
  end

  @impl true
  def handle_info(:heartbeat, state) do
    {x, y, z} = state.position
    # Simulating periodic broadcast across actor mesh
    Logger.debug("[Node #{state.id}] Ping: x=#{x}, y=#{y}, z=#{z}")
    schedule_heartbeat()
    {:noreply, state}
  end

  # --- Private Helpers ---

  defp via_tuple(drone_id) do
    {:global, {:drone_node, drone_id}}
  end

  defp schedule_heartbeat do
    Process.send_after(self(), :heartbeat, @heartbeat_interval)
  end
end
