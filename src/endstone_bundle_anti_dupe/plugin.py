from endstone.plugin import Plugin
from endstone.event import EventPriority, event_handler, PlayerInteractEvent

class AntiBundleDuping(Plugin):
    api_version = "0.11"
    def on_load(self):
        self.logger.info("Anti-Bundle-Duping has been loaded!")

    def on_enable(self):
        self.logger.info("Anti-Bundle-Duping has been enabled!")
        self.register_events(self)
    
    @event_handler(priority=EventPriority.HIGH)
    def on_player_interact(self, event: PlayerInteractEvent):
        block = event.block
        if not block:
            return
        if "hopper" in block.type.name.lower():
            player = event.player
            """Make the player can't put bundles inside hoppers"""
            