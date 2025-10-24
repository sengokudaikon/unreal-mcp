#include "Commands/UnrealMCPBlueprintCommands.h"

#include "Commands/Blueprint/CreateBlueprint.h"
#include "Commands/Blueprint/CompileBlueprint.h"
#include "Commands/Blueprint/SpawnBlueprint.h"
#include "Commands/Blueprint/SetComponentProperty.h"
#include "Commands/Blueprint/SetPhysicsProperties.h"
#include "Commands/Blueprint/SetBlueprintProperty.h"
#include "Commands/Blueprint/SetStaticMeshProperties.h"
#include "Commands/Blueprint/SetPawnProperties.h"
#include "Commands/CommonUtils.h"
#include "Commands/Blueprint/AddComponent.h"

FUnrealMCPBlueprintCommands::FUnrealMCPBlueprintCommands() {
	CommandHandlers.Add(TEXT("create_blueprint"), &FCreateBlueprint::Handle);
	CommandHandlers.Add(TEXT("compile_blueprint"), &FCompileBlueprint::Handle);
	CommandHandlers.Add(TEXT("spawn_blueprint_actor"), &FSpawnBlueprint::Handle);
	CommandHandlers.Add(TEXT("add_component_to_blueprint"), &FAddComponent::Handle);
	CommandHandlers.Add(TEXT("set_component_property"), &FSetComponentProperty::Handle);
	CommandHandlers.Add(TEXT("set_physics_properties"), &FSetPhysicsProperties::Handle);
	CommandHandlers.Add(TEXT("set_blueprint_property"), &FSetBlueprintProperty::Handle);
	CommandHandlers.Add(TEXT("set_static_mesh_properties"), &FSetStaticMeshProperties::Handle);
	CommandHandlers.Add(TEXT("set_pawn_properties"), &FSetPawnProperties::Handle);
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
