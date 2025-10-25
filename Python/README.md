# Unreal MCP Python Server

Python bridge for interacting with Unreal Engine 5.5 using the Model Context Protocol (MCP).

## Installation

### Development Setup

```bash
# Install with development dependencies
pip install -e .[dev]

# Or use the Makefile
make install-dev
```

### Quick Setup with uv

1. Make sure Python 3.10+ is installed
2. Install `uv` if you haven't already:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. Create and activate a virtual environment:
   ```bash
   uv venv
   source .venv/bin/activate  # On Unix/macOS
   # or
   .venv\Scripts\activate     # On Windows
   ```
4. Install dependencies:
   ```bash
   uv pip install -e .[dev]
   ```

### Running the Server Manually

```bash
python server.py
```

### Available Tools

#### Blueprint Tools
- `create_blueprint(name, parent_class)` - Create new Blueprint classes
- `spawn_blueprint_actor(blueprint_name, actor_name, location, rotation, scale)` - Spawn actors
- `add_component_to_blueprint(...)` - Add components with type-safe parameters
- `set_static_mesh_properties(...)` - Configure static meshes
- `set_physics_properties(...)` - Configure physics with validation
- `compile_blueprint(blueprint_name)` - Compile Blueprint changes

#### Editor Tools
- `get_actors_in_level()` - List all actors in current level
- `find_actors_by_name(pattern)` - Find actors by name pattern
- `spawn_actor(...)` - Create actors with transform
- `delete_actor(name)` - Remove actors
- `set_actor_transform(...)` - Modify actor transforms
- `focus_viewport(...)` - Focus viewport on targets
- `take_screenshot(...)` - Capture screenshots

#### UMG Tools
- `create_umg_widget_blueprint(...)` - Create widget blueprints
- `add_text_block_to_widget(...)` - Add text with styling
- `add_button_to_widget(...)` - Add buttons with events
- `bind_widget_event(...)` - Bind widget events
- `add_widget_to_viewport(...)` - Add widgets to viewport

#### Project Tools
- `create_input_mapping(...)` - Create input mappings

## Development

### Code Quality

```bash
# Format code
make format

# Check formatting
make format-check

# Run linting
make lint

# Type checking
make type-check

# Security checks
make security

# Run all checks
make pre-commit
```

### Testing

```bash
# Run unit tests
make test

# Run tests with coverage
make test-cov

# Run integration tests
make test-integration

# Run all tests
make test-all
```

## Troubleshooting

- Make sure Unreal Engine editor is loaded and running before running the server
- Check logs in `unreal_mcp.log` for detailed error information
- Ensure proper MCP client configuration