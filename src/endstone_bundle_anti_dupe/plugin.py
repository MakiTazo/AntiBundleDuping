from endstone.plugin import Plugin
from endstone.event import EventPriority, event_handler, PlayerInteractEvent, PlayerInteractActorEvent, PlayerDropItemEvent

class AntiBundleDuping(Plugin):
    api_version = "0.11"
    
    BLOCKED_CONTAINERS = ["hopper", "chest", "barrel", "shulker_box", "dropper"]
    BLOCKED_ENTITIES = ["chest", "hopper"]
    
    def on_load(self):
        self.logger.info("Anti-Bundle-Duping has been loaded!")

    def on_enable(self):
        self.logger.info("Anti-Bundle-Duping has been enabled!")
        self.register_events(self)
    
    def is_block_container(self, block_type) -> bool:
        for container in self.BLOCKED_CONTAINERS:
            if container in block_type:
                return True
        return False
    
    def is_entity_container(self, entity_type) -> bool:
        for container in self.BLOCKED_ENTITIES:
            if container in entity_type:
                return True
        return False
    
    def has_bundle_in_inventory(self, player) -> bool:
        for item in player.inventory.contents:
            if item and "bundle" in item.type.id:
                return True
        main_hand = player.inventory.item_in_main_hand
        off_hand = player.inventory.item_in_off_hand
        return (main_hand and "bundle" in main_hand.type.id) or \
               (off_hand and "bundle" in off_hand.type.id)
    
    def cancel_interaction(self, player, message):
        player.send_message("§cYou can't use a container while having a bundle in your inventory to prevent duping exploits!")
        self.logger.info(f"Duping attempt prevented for {player.name}")
    
    @event_handler(priority=EventPriority.HIGH)
    def on_player_interact(self, event: PlayerInteractEvent):
        block = event.block
        if not block or not self.is_block_container(block.type):
            return
        
        if self.has_bundle(event.player):
            event.is_cancelled = True
            self.cancel_interaction(event.player, block.type)
    
    @event_handler(priority=EventPriority.HIGH)
    def on_player_interact_actor(self, event: PlayerInteractActorEvent):
        actor_type = event.actor.type
        if not actor_type or not self.is_entity_container(actor_type):
            return
        
        if self.has_bundle(event.player):
            event.is_cancelled = True
            self.cancel_interaction(event.player, str(actor_type))
            
    @event_handler(priority=EventPriority.HIGH)
    def on_player_drop_item(self, event: PlayerDropItemEvent):
        item_type = event.item.type
        if item_type and "bundle" in item_type.id:
            # BUG: When cancelling the drop event, the item disappears from the player's inventory.
            event.is_cancelled = True
            event.player.send_message("§cYou can't drop a bundle to prevent duping exploits!")
            self.logger.info(f"Duping attempt prevented for {event.player.name} by dropping a bundle")
    