from endstone.plugin import Plugin
from endstone.event import EventPriority, event_handler, PacketSendEvent, PlayerInteractEvent

class AntiBundleDuping(Plugin):
    api_version = "0.11"
    
    def on_load(self):
        self.logger.info("Anti-Bundle-Duping loaded!")

    def on_enable(self):
        self.logger.info("Anti-Bundle-Duping enabled!")
        self.register_events(self)
        self.last_hopper = {}
        self.hoppers_to_clean = set()
        
        # Scheduler para limpiar tolvas marcadas
        self.server.scheduler.run_task(
            self,
            self.clean_marked_hoppers,
            period=1  # Cada tick
        )
    
    @event_handler
    def on_player_interact(self, event: PlayerInteractEvent):
        if not event.block or "hopper" not in event.block.type:
            return
        
        player = event.player
        # Guardar ubicación como enteros para evitar problemas
        self.last_hopper[player.name] = (event.block.x, event.block.y, event.block.z)
    
    @event_handler(priority=EventPriority.MONITOR)
    def on_packet_send(self, event: PacketSendEvent):
        if event.packet_id != 49:
            return
        if b'bundle' not in event.payload.lower():
            return
        player = event.player
        if not player or player.name not in self.last_hopper:
            return
        hopper_pos = self.last_hopper[player.name]
        self.hoppers_to_clean.add(hopper_pos)
        self.logger.info(f"Hopper marked for cleaning: {hopper_pos}")
    
    def clean_marked_hoppers(self):
        if not self.hoppers_to_clean:
            return
        level = self.server.level
        for hopper_pos in list(self.hoppers_to_clean):
            x, y, z = hopper_pos
            for dimension in level.dimensions:
                try:
                    block = dimension.get_block_at(int(x), int(y), int(z))
                    if "hopper" in block.type:
                        block.set_type("minecraft:air", apply_physics=False)
                        block.set_type("minecraft:hopper", apply_physics=False)
                        self.logger.info(f"Cleaned Hopper in: {hopper_pos}")
                except Exception as e:
                    self.logger.warning(f"Error while cleaning executing: {e}")
            
            self.hoppers_to_clean.remove(hopper_pos)