# AntiBundleDuping

[![Endstone](https://img.shields.io/badge/Endstone-0.11-blue.svg)](https://endstone.dev)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENCE)

Automatically removes bundles from hoppers on Minecraft Bedrock Edition servers running the Endstone engine, preventing duplication exploits.

## 🎯 Overview

**AntiBundleDuping** is a lightweight plugin for Endstone that monitors hoppers in real-time and automatically replaces any hopper containing a bundle with a clean, empty one. This effectively prevents duplication exploits where bundles interact with hoppers to duplicate items, without restricting legitimate player interactions.

Instead of blocking players from using containers — which proved ineffective against creative exploit methods — this plugin takes a direct approach: it detects bundles inside hoppers at the packet level and resets the hopper immediately, breaking any duplication mechanics while keeping the hopper functional for normal use.

## ✨ Features

- 🔍 **Packet-level detection** — Monitors inventory packets sent to players and detects bundles inside hoppers instantly
- 🔄 **Automatic hopper reset** — Replaces affected hoppers with fresh empty ones in 2 ticks, dropping the bundle as a world item
- 🧹 **Non-intrusive** — Players can interact freely with all containers; the plugin silently cleans hoppers in the background
- 📊 **Console logging** — Logs every detection and hopper reset with location details for server administrators
- ⚡ **Lightweight** — Minimal performance impact using event-driven architecture with scheduled safe block operations

## 📋 Requirements

- **Endstone** 0.11 or higher
- **Minecraft Bedrock** 1.21.60 or higher

## 🚀 Installation

1. Download the latest `.whl` file from the releases page
2. Place it in your server's `plugins/` directory
3. Restart your server
4. The plugin will automatically start monitoring hoppers — no configuration needed

## 🔧 How It Works

1. When a player opens a hopper, the plugin remembers which hopper was accessed
2. If the server sends inventory data containing a bundle (`minecraft:bundle`), the plugin marks that hopper for cleaning
3. On the next server tick, the hopper is replaced with air (dropping its contents)
4. On the following tick, a new empty hopper is placed in the same location
5. The bundle falls as a world item and cannot be used for duplication

## 📝 Notes

- The hopper replacement resets the hopper's orientation to facing down (default state)
- This is intentional and helps break dupe mechanics that rely on specific hopper orientations
- Bundles dropped on the ground will not be picked up by the new hopper immediately due to the 2-tick reset window
- No player permissions or commands are required — the plugin works fully automatically

## 📄 License

This project is licensed under the MIT License — see the [LICENCE](./LICENCE) file for details.