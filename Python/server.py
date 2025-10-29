"""
Unreal Engine MCP Server

A clean, service-oriented MCP server for interacting with Unreal Engine.
"""

import logging
import sys
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Dict

from mcp.server.fastmcp import FastMCP

from core.errors import UnrealMCPError

# Core imports
from services.service_manager import initialize_services, shutdown_services

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
    handlers=[
        logging.FileHandler("unreal_mcp.log"),
    ],
)
logger = logging.getLogger("UnrealMCP")


@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[Dict[str, Any]]:
    """Handle server startup and shutdown."""
    logger.info("UnrealMCP server starting up")

    try:
        # Initialize services
        initialize_services()
        logger.info("Services initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing services: {e}")
        # Continue anyway - services will try to connect on demand

    try:
        yield {}
    finally:
        logger.info("Shutting down services")
        shutdown_services()
        logger.info("Unreal MCP server shut down")


# Initialize server
mcp = FastMCP("UnrealMCP", lifespan=server_lifespan)

# Register tools
from tools.blueprint_node_tools import register_blueprint_node_tools
from tools.blueprint_tools import register_blueprint_tools
from tools.editor_tools import register_editor_tools
from tools.input_tools import register_input_tools
from tools.project_tools import register_project_tools
from tools.registry_tools import register_registry_tools
from tools.umg_tools import register_umg_tools

# Register all tools
register_blueprint_tools(mcp)
register_blueprint_node_tools(mcp)
register_editor_tools(mcp)
register_input_tools(mcp)
register_umg_tools(mcp)
register_project_tools(mcp)
register_registry_tools(mcp)


@mcp.prompt()
def info():
    """Information about available Unreal MCP tools and best practices."""
    return """
    # Unreal MCP Server Tools and Best Practices

    ## Architecture
    This server uses a clean service-oriented architecture with:
    - **Core Layer**: Type-safe parameters, connection management, error handling
    - **Services Layer**: High-level business logic for different Unreal domains
    - **Tools Layer**: Thin MCP tool wrappers that delegate to services

    ## Available Tools

    ### Blueprint Tools
    - `create_blueprint(name, parent_class)` - Create new Blueprint classes
    - `spawn_blueprint_actor(blueprint_name, actor_name, location, rotation, scale)` - Spawn actors
    - `add_component_to_blueprint(...)` - Add components with type-safe parameters
    - `set_static_mesh_properties(...)` - Configure static meshes
    - `set_physics_properties(...)` - Configure physics with validation
    - `compile_blueprint(blueprint_name)` - Compile Blueprint changes
    - `set_blueprint_property(...)` - Set Blueprint properties
    - `list_blueprints()` - List all available blueprints in the project
    - `blueprint_exists(blueprint_name)` - Check if a blueprint exists
    - `get_blueprint_info(blueprint_name)` - Get detailed blueprint information
    - `get_blueprint_components(blueprint_name)` - Get all blueprint components
    - `get_blueprint_variables(blueprint_name)` - Get all blueprint variables
    - `get_blueprint_functions(blueprint_name)` - Get all blueprint functions
    - `get_component_properties(...)` - Get component properties
    - `set_component_property(...)` - Set component properties
    - `remove_component(...)` - Remove components from blueprints
    - `rename_component(...)` - Rename blueprint components
    - `get_blueprint_path(blueprint_name)` - Get blueprint file path
    - `get_component_hierarchy(blueprint_name)` - Get component hierarchy
    - `set_component_transform(...)` - Set component transforms
    - `delete_blueprint(blueprint_name)` - Delete blueprints
    - `duplicate_blueprint(...)` - Duplicate blueprints with new names

    ### Blueprint Node Tools
    - `connect_blueprint_nodes(...)` - Connect two blueprint nodes via their pins
    - `add_blueprint_event_node(...)` - Add event nodes to blueprint graphs
    - `add_blueprint_function_node(...)` - Add function call nodes to blueprint graphs
    - `add_blueprint_variable(...)` - Add variables to blueprints
    - `find_blueprint_nodes(...)` - Find nodes in blueprint graphs by type and criteria
    - `add_blueprint_input_action_node(...)` - Add legacy input action nodes
    - `add_blueprint_self_reference_node(...)` - Add self reference nodes
    - `add_blueprint_get_self_component_reference_node(...)` - Add self component reference nodes

    ### Editor Tools
    - `get_actors_in_level()` - List all actors in current level
    - `find_actors_by_name(pattern)` - Find actors by name pattern
    - `spawn_actor(...)` - Create actors with transform
    - `delete_actor(name)` - Remove actors
    - `set_actor_transform(...)` - Modify actor transforms
    - `get_actor_properties(name)` - Get actor properties
    - `set_actor_property(...)` - Set actor properties by name
    - `focus_viewport(...)` - Focus viewport on targets
    - `take_screenshot(...)` - Capture screenshots

    ### Input Tools
    - `create_enhanced_input_action(...)` - Create Enhanced Input Action assets
    - `create_input_mapping_context(...)` - Create Input Mapping Context assets
    - `add_enhanced_input_mapping(...)` - Add key mappings to contexts
    - `remove_enhanced_input_mapping(...)` - Remove key mappings from contexts
    - `apply_mapping_context(...)` - Apply mapping contexts with priority
    - `remove_mapping_context(...)` - Remove applied mapping contexts
    - `clear_all_mapping_contexts()` - Clear all applied mapping contexts

    ### UMG Tools
    - `create_widget_blueprint(...)` - Create widget blueprints
    - `add_text_block(...)` - Add text with styling
    - `add_button(...)` - Add buttons with events
    - `bind_widget_event(...)` - Bind widget events
    - `add_widget_to_viewport(...)` - Add widgets to viewport
    - `set_text_block_binding(...)` - Set dynamic bindings

    ### Project Tools
    - `create_legacy_input_mapping(...)` - Create legacy input mappings (deprecated)

    ### Registry Tools
    - `get_available_api_methods()` - Get all available API methods organized by category
    - `get_supported_parent_classes()` - Get all supported parent classes for Blueprint creation
    - `get_supported_component_types()` - Get all supported component types

    ## Benefits of New Architecture

    ### Type Safety
    - All parameters are validated at runtime
    - Vector3, Transform, and other parameter objects prevent errors
    - Clear error messages for invalid parameters

    ### Maintainability
    - Clear separation of concerns
    - Services can be tested independently
    - Consistent error handling across all tools

    ### Reliability
    - Robust connection management
    - Automatic reconnection on failures
    - Proper resource cleanup

    ### Extensibility
    - Easy to add new services and tools
    - Shared utilities and common patterns
    - Service layer handles complex logic
    """


if __name__ == "__main__":
    logger.info("Starting MCP server with stdio transport")
    try:
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)
