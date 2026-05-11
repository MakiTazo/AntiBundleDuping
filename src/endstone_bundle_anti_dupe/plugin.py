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
        if not block or "hopper" not in block.type:
            return
        player = event.player
        has_bundle = False
        
        for item in player.inventory.contents:
            if item and "bundle" in item.type.id:
                has_bundle = True
                break
            
        if not has_bundle:
            main_hand = player.inventory.item_in_main_hand
            off_hand = player.inventory.item_in_off_hand
            if (main_hand and "bundle" in main_hand.type.id) or \
                (off_hand and "bundle" in off_hand.type.id):
                has_bundle = True
        if has_bundle:
            event.is_cancelled = True
            player.send_message(
                "§cYou can't use a hopper while holding a bundle to prevent duping exploits!")
            self.logger.info(f"A duping exploit attempt was prevented for {player.name}")