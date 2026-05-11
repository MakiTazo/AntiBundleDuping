# AntiBundleDuping

[![Endstone](https://img.shields.io/badge/Endstone-0.11-blue.svg)](https://endstone.dev)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Prevents item duplication exploits involving bundles and hoppers on Minecraft Bedrock Edition servers running the Endstone engine.

## 🎯 Overview

**AntiBundleDuping** is a lightweight plugin for Endstone that blocks players from interacting with hoppers while they have a bundle in their inventory. This effectively prevents a known duplication exploit where bundles interact with hoppers to duplicate items.

## ✨ Features

- ✅ **Automatically detects bundles** in player inventories (main inventory, hotbar, and off-hand)
- 🚫 **Blocks hopper interactions** when a bundle is present
- 📊 **Console logging** for see who is the mf who is trying to use the bundle on a hopper

## 📋 Requirements

- **Endstone** 0.11 or higher

## 🚀 Installation

1. Download the latest `whl` file
2. Place it in your server's `plugins/` directory
3. Restart your server
4. The plugin will automatically start preventing for dupers