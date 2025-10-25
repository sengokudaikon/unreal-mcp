﻿#include "Commands/UnrealMCPBlueprintCommands.h"

#include "Commands/Blueprint/CreateBlueprint.h"
#include "Commands/Blueprint/CompileBlueprint.h"
#include "Commands/Blueprint/SpawnActorBlueprint.h"
#include "Commands/Blueprint/SetComponentProperty.h"
#include "Commands/Blueprint/SetPhysicsProperties.h"
#include "Commands/Blueprint/SetBlueprintProperty.h"
#include "Commands/Blueprint/SetStaticMeshProperties.h"
#include "Commands/Blueprint/SetPawnProperties.h"
#include "Commands/Blueprint/AddComponent.h"
#include "Commands/Blueprint/ListBlueprints.h"
#include "Commands/Blueprint/BlueprintIntrospectionCommands.h"
#include "Commands/CommonUtils.h"

FUnrealMCPBlueprintCommands::FUnrealMCPBlueprintCommands() {
	using namespace UnrealMCP;

	CommandHandlers.Add(TEXT("create_blueprint"), &FCreateBlueprint::Handle);
	CommandHandlers.Add(TEXT("compile_blueprint"), &FCompileBlueprint::Handle);
	CommandHandlers.Add(TEXT("spawn_blueprint_actor"), &FSpawnActorBlueprint::Handle);
	CommandHandlers.Add(TEXT("add_component_to_blueprint"), &FAddComponent::Handle);
	CommandHandlers.Add(TEXT("set_component_property"), &FSetComponentProperty::Handle);
	CommandHandlers.Add(TEXT("set_physics_properties"), &FSetPhysicsProperties::Handle);
	CommandHandlers.Add(TEXT("set_blueprint_property"), &FSetBlueprintProperty::Handle);
	CommandHandlers.Add(TEXT("set_static_mesh_properties"), &FSetStaticMeshProperties::Handle);
	CommandHandlers.Add(TEXT("set_pawn_properties"), &FSetPawnProperties::Handle);

	CommandHandlers.Add(TEXT("list_blueprints"), &FListBlueprintsCommand::Execute);
	CommandHandlers.Add(TEXT("blueprint_exists"), &FBlueprintExistsCommand::Execute);
	CommandHandlers.Add(TEXT("get_blueprint_info"), &FGetBlueprintInfoCommand::Execute);
	CommandHandlers.Add(TEXT("get_blueprint_components"), &FGetBlueprintComponentsCommand::Execute);
	CommandHandlers.Add(TEXT("get_blueprint_variables"), &FGetBlueprintVariablesCommand::Execute);
	CommandHandlers.Add(TEXT("get_blueprint_path"), &FGetBlueprintPathCommand::Execute);
}

TSharedPtr<FJsonObject> FUnrealMCPBlueprintCommands::HandleCommand(
	const FString& CommandType,
	const TSharedPtr<FJsonObject>& Params
) {
	if (const auto* Handler = CommandHandlers.Find(CommandType)) {
		return (*Handler)(Params);
	}

	return FCommonUtils::CreateErrorResponse(FString::Printf(TEXT("Unknown blueprint command: %s"), *CommandType));
}
