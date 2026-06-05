from endstone.plugin import Plugin
from endstone.event import event_handler, PacketSendEvent, PlayerInteractEvent

class AntiBundleDuping(Plugin):
    api_version = "0.11"

    def on_enable(self):
        self.logger.info("Anti-Bundle-Duping enabled!")
        self.register_events(self)
        self.last_hopper = {}
        self.hoppers_to_clean = set()
        self.server.scheduler.run_task(
            self,
            self.clean_marked_hoppers,
            period=1
        )
        self.server.scheduler.run_task(
            self,
            self.check_marked_players,
            period=20
        )

    @event_handler
    def on_player_interact(self, event: PlayerInteractEvent):
        if not event.block or "hopper" not in event.block.type:
            self.last_hopper.pop(event.player.name, None)
            return

        player = event.player
        self.last_hopper[player.name] = (event.block.x, event.block.y, event.block.z)

    @event_handler
    def on_packet_send(self, event: PacketSendEvent):
        if event.packet_id != 49:
            return
        if b'bundle' not in event.payload.lower():
            return

        player = event.player
        if not player or player.name not in self.last_hopper:
            return

        hopper_pos = self.last_hopper.pop(player.name)  # ← limpiar tras usar
        self.hoppers_to_clean.add(hopper_pos)
        self.logger.info(f"Intento de duping en: {hopper_pos} por {player.name}")

    def clean_marked_hoppers(self):
        if not self.hoppers_to_clean:
            return

        level = self.server.level
        for hopper_pos in list(self.hoppers_to_clean):
            x, y, z = hopper_pos
            try:
                for dimension in level.dimensions:
                    block = dimension.get_block_at(int(x), int(y), int(z))
                    if "hopper" in block.type:
                        block.set_type("minecraft:air", apply_physics=False)
                        block.set_type("minecraft:hopper", apply_physics=False)
                        self.logger.info(f"Hopper limpiado en: {hopper_pos}")
            except Exception as e:
                self.logger.warning(f"Error while cleaning: {e}")
            finally:
                self.hoppers_to_clean.discard(hopper_pos)

    def check_marked_players(self):
        for player_name in list(self.last_hopper.keys()):
            player = self.server.get_player(player_name)
            if not player:
                self.last_hopper.pop(player_name, None)
                continue
            has_bundle = any(
                item and "bundle" in str(item.type)
                for item in player.inventory.contents
            )
            if not has_bundle:
                self.last_hopper.pop(player_name, None)
