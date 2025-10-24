#include "Core/MCPTypes.h"
#include "Commands/CommonUtils.h"

namespace UnrealMCP {
	auto FBlueprintSpawnParams::FromJson(const TSharedPtr<FJsonObject>& Json) -> TResult<FBlueprintSpawnParams> {
		if (!Json.IsValid()) {
			return TResult<FBlueprintSpawnParams>::Failure(TEXT("Invalid JSON object"));
		}

		FBlueprintSpawnParams Params;

		// Required fields
		if (!Json->TryGetStringField(TEXT("blueprint_name"), Params.BlueprintName)) {
			return TResult<FBlueprintSpawnParams>::Failure(TEXT("Missing 'blueprint_name' parameter"));
		}

		if (!Json->TryGetStringField(TEXT("actor_name"), Params.ActorName)) {
			return TResult<FBlueprintSpawnParams>::Failure(TEXT("Missing 'actor_name' parameter"));
		}

		// Optional fields
		if (Json->HasField(TEXT("location"))) {
			Params.Location = FCommonUtils::GetVectorFromJson(Json, TEXT("location"));
		}

		if (Json->HasField(TEXT("rotation"))) {
			Params.Rotation = FCommonUtils::GetRotatorFromJson(Json, TEXT("rotation"));
		}

		return TResult<FBlueprintSpawnParams>::Success(MoveTemp(Params));
	}

	auto FBlueprintCreationParams::FromJson(const TSharedPtr<FJsonObject>& Json) -> TResult<FBlueprintCreationParams> {
		if (!Json.IsValid()) {
			return TResult<FBlueprintCreationParams>::Failure(TEXT("Invalid JSON object"));
		}

		FBlueprintCreationParams Params;

		// Required fields
		if (!Json->TryGetStringField(TEXT("name"), Params.Name)) {
			return TResult<FBlueprintCreationParams>::Failure(TEXT("Missing 'name' parameter"));
		}

		// Optional fields
		Json->TryGetStringField(TEXT("parent_class"), Params.ParentClass);

		FString PackagePath;
		if (Json->TryGetStringField(TEXT("package_path"), PackagePath)) {
			Params.PackagePath = PackagePath;
		}

		return TResult<FBlueprintCreationParams>::Success(MoveTemp(Params));
	}

	auto FComponentParams::FromJson(const TSharedPtr<FJsonObject>& Json) -> TResult<FComponentParams> {
		if (!Json.IsValid()) {
			return TResult<FComponentParams>::Failure(TEXT("Invalid JSON object"));
		}

		FComponentParams Params;

		// Required fields
		if (!Json->TryGetStringField(TEXT("blueprint_name"), Params.BlueprintName)) {
			return TResult<FComponentParams>::Failure(TEXT("Missing 'blueprint_name' parameter"));
		}

		if (!Json->TryGetStringField(TEXT("component_type"), Params.ComponentType)) {
			return TResult<FComponentParams>::Failure(TEXT("Missing 'component_type' parameter"));
		}

		if (!Json->TryGetStringField(TEXT("component_name"), Params.ComponentName)) {
			return TResult<FComponentParams>::Failure(TEXT("Missing 'component_name' parameter"));
		}

		// Optional fields
		FString MeshType;
		if (Json->TryGetStringField(TEXT("static_mesh"), MeshType)) {
			Params.MeshType = MeshType;
		}

		if (Json->HasField(TEXT("location"))) {
			Params.Location = FCommonUtils::GetVectorFromJson(Json, TEXT("location"));
		}

		if (Json->HasField(TEXT("rotation"))) {
			Params.Rotation = FCommonUtils::GetRotatorFromJson(Json, TEXT("rotation"));
		}

		if (Json->HasField(TEXT("scale"))) {
			Params.Scale = FCommonUtils::GetVectorFromJson(Json, TEXT("scale"));
		}

		if (Json->HasField(TEXT("component_properties"))) {
			Params.Properties = Json->GetObjectField(TEXT("component_properties"));
		}

		return TResult<FComponentParams>::Success(MoveTemp(Params));
	}

	auto FPropertyParams::FromJson(const TSharedPtr<FJsonObject>& Json,
	                               const FString& TargetFieldName) -> TResult<FPropertyParams> {
		if (!Json.IsValid()) {
			return TResult<FPropertyParams>::Failure(TEXT("Invalid JSON object"));
		}

		FPropertyParams Params;

		// Required fields
		if (!Json->TryGetStringField(*TargetFieldName, Params.TargetName)) {
			return TResult<FPropertyParams>::Failure(FString::Printf(TEXT("Missing '%s' parameter"), *TargetFieldName));
		}

		if (!Json->TryGetStringField(TEXT("property_name"), Params.PropertyName)) {
			return TResult<FPropertyParams>::Failure(TEXT("Missing 'property_name' parameter"));
		}

		if (!Json->HasField(TEXT("property_value"))) {
			return TResult<FPropertyParams>::Failure(TEXT("Missing 'property_value' parameter"));
		}

		Params.PropertyValue = Json->Values.FindRef(TEXT("property_value"));

		return TResult<FPropertyParams>::Success(MoveTemp(Params));
	}

	auto FPhysicsParams::FromJson(const TSharedPtr<FJsonObject>& Json) -> TResult<FPhysicsParams> {
		if (!Json.IsValid()) {
			return TResult<FPhysicsParams>::Failure(TEXT("Invalid JSON object"));
		}

		FPhysicsParams Params;

		// Required fields
		if (!Json->TryGetStringField(TEXT("blueprint_name"), Params.BlueprintName)) {
			return TResult<FPhysicsParams>::Failure(TEXT("Missing 'blueprint_name' parameter"));
		}

		if (!Json->TryGetStringField(TEXT("component_name"), Params.ComponentName)) {
			return TResult<FPhysicsParams>::Failure(TEXT("Missing 'component_name' parameter"));
		}

		// Optional fields with defaults
		if (Json->HasField(TEXT("simulate_physics"))) {
			Params.bSimulatePhysics = Json->GetBoolField(TEXT("simulate_physics"));
		}

		if (Json->HasField(TEXT("mass"))) {
			Params.Mass = Json->GetNumberField(TEXT("mass"));
		}

		if (Json->HasField(TEXT("linear_damping"))) {
			Params.LinearDamping = Json->GetNumberField(TEXT("linear_damping"));
		}

		if (Json->HasField(TEXT("angular_damping"))) {
			Params.AngularDamping = Json->GetNumberField(TEXT("angular_damping"));
		}

		if (Json->HasField(TEXT("gravity_enabled"))) {
			Params.bEnableGravity = Json->GetBoolField(TEXT("gravity_enabled"));
		}

		return TResult<FPhysicsParams>::Success(MoveTemp(Params));
	}

	auto FWidgetCreationParams::FromJson(const TSharedPtr<FJsonObject>& Json) -> TResult<FWidgetCreationParams> {
		if (!Json.IsValid()) {
			return TResult<FWidgetCreationParams>::Failure(TEXT("Invalid JSON object"));
		}

		FWidgetCreationParams Params;

		// Required fields
		if (!Json->TryGetStringField(TEXT("name"), Params.Name)) {
			return TResult<FWidgetCreationParams>::Failure(TEXT("Missing 'name' parameter"));
		}

		// Optional fields with defaults
		Json->TryGetStringField(TEXT("parent_class"), Params.ParentClass);

		FString PackagePath;
		if (Json->TryGetStringField(TEXT("path"), PackagePath)) {
			Params.PackagePath = PackagePath;
		}

		return TResult<FWidgetCreationParams>::Success(MoveTemp(Params));
	}

	auto FTextBlockParams::FromJson(const TSharedPtr<FJsonObject>& Json) -> TResult<FTextBlockParams> {
		if (!Json.IsValid()) {
			return TResult<FTextBlockParams>::Failure(TEXT("Invalid JSON object"));
		}

		FTextBlockParams Params;

		// Required fields
		if (!Json->TryGetStringField(TEXT("widget_name"), Params.WidgetName)) {
			return TResult<FTextBlockParams>::Failure(TEXT("Missing 'widget_name' parameter"));
		}

		if (!Json->TryGetStringField(TEXT("text_block_name"), Params.TextBlockName)) {
			return TResult<FTextBlockParams>::Failure(TEXT("Missing 'text_block_name' parameter"));
		}

		// Optional fields with defaults
		Json->TryGetStringField(TEXT("text"), Params.Text);

		if (Json->HasField(TEXT("position"))) {
			Params.Position = FCommonUtils::GetVector2DFromJson(Json, TEXT("position"));
		}

		if (Json->HasField(TEXT("size"))) {
			Params.Size = FCommonUtils::GetVector2DFromJson(Json, TEXT("size"));
		}

		if (Json->HasField(TEXT("font_size"))) {
			Params.FontSize = static_cast<int32>(Json->GetNumberField(TEXT("font_size")));
		}

		return TResult<FTextBlockParams>::Success(MoveTemp(Params));
	}

	auto FButtonParams::FromJson(const TSharedPtr<FJsonObject>& Json) -> TResult<FButtonParams> {
		if (!Json.IsValid()) {
			return TResult<FButtonParams>::Failure(TEXT("Invalid JSON object"));
		}

		FButtonParams Params;

		// Required fields
		if (!Json->TryGetStringField(TEXT("widget_name"), Params.WidgetName)) {
			return TResult<FButtonParams>::Failure(TEXT("Missing 'widget_name' parameter"));
		}

		if (!Json->TryGetStringField(TEXT("button_name"), Params.ButtonName)) {
			return TResult<FButtonParams>::Failure(TEXT("Missing 'button_name' parameter"));
		}

		// Optional fields with defaults
		Json->TryGetStringField(TEXT("text"), Params.Text);

		if (Json->HasField(TEXT("position"))) {
			Params.Position = FCommonUtils::GetVector2DFromJson(Json, TEXT("position"));
		}

		if (Json->HasField(TEXT("size"))) {
			Params.Size = FCommonUtils::GetVector2DFromJson(Json, TEXT("size"));
		}

		if (Json->HasField(TEXT("font_size"))) {
			Params.FontSize = static_cast<int32>(Json->GetNumberField(TEXT("font_size")));
		}

		return TResult<FButtonParams>::Success(MoveTemp(Params));
	}

	auto FWidgetEventBindingParams::FromJson(const TSharedPtr<FJsonObject>& Json) -> TResult<FWidgetEventBindingParams> {
		if (!Json.IsValid()) {
			return TResult<FWidgetEventBindingParams>::Failure(TEXT("Invalid JSON object"));
		}

		FWidgetEventBindingParams Params;

		// Required fields
		if (!Json->TryGetStringField(TEXT("widget_name"), Params.WidgetName)) {
			return TResult<FWidgetEventBindingParams>::Failure(TEXT("Missing 'widget_name' parameter"));
		}

		if (!Json->TryGetStringField(TEXT("widget_component_name"), Params.WidgetComponentName)) {
			return TResult<FWidgetEventBindingParams>::Failure(TEXT("Missing 'widget_component_name' parameter"));
		}

		if (!Json->TryGetStringField(TEXT("event_name"), Params.EventName)) {
			return TResult<FWidgetEventBindingParams>::Failure(TEXT("Missing 'event_name' parameter"));
		}

		// Optional fields with defaults
		if (Json->TryGetStringField(TEXT("function_name"), Params.FunctionName)) {
			// Use provided function name
		} else {
			// Default function name
			Params.FunctionName = Params.WidgetComponentName + TEXT("_") + Params.EventName;
		}

		return TResult<FWidgetEventBindingParams>::Success(MoveTemp(Params));
	}

	auto FTextBlockBindingParams::FromJson(const TSharedPtr<FJsonObject>& Json) -> TResult<FTextBlockBindingParams> {
		if (!Json.IsValid()) {
			return TResult<FTextBlockBindingParams>::Failure(TEXT("Invalid JSON object"));
		}

		FTextBlockBindingParams Params;

		// Required fields
		if (!Json->TryGetStringField(TEXT("widget_name"), Params.WidgetName)) {
			return TResult<FTextBlockBindingParams>::Failure(TEXT("Missing 'widget_name' parameter"));
		}

		if (!Json->TryGetStringField(TEXT("text_block_name"), Params.TextBlockName)) {
			return TResult<FTextBlockBindingParams>::Failure(TEXT("Missing 'text_block_name' parameter"));
		}

		if (!Json->TryGetStringField(TEXT("binding_property"), Params.BindingProperty)) {
			return TResult<FTextBlockBindingParams>::Failure(TEXT("Missing 'binding_property' parameter"));
		}

		// Optional fields with defaults
		Json->TryGetStringField(TEXT("binding_type"), Params.BindingType);

		return TResult<FTextBlockBindingParams>::Success(MoveTemp(Params));
	}

	auto FAddWidgetToViewportParams::FromJson(const TSharedPtr<FJsonObject>& Json) -> TResult<FAddWidgetToViewportParams> {
		if (!Json.IsValid()) {
			return TResult<FAddWidgetToViewportParams>::Failure(TEXT("Invalid JSON object"));
		}

		FAddWidgetToViewportParams Params;

		// Required fields
		if (!Json->TryGetStringField(TEXT("widget_name"), Params.WidgetName)) {
			return TResult<FAddWidgetToViewportParams>::Failure(TEXT("Missing 'widget_name' parameter"));
		}

		// Optional fields with defaults
		if (Json->HasField(TEXT("z_order"))) {
			Params.ZOrder = static_cast<int32>(Json->GetNumberField(TEXT("z_order")));
		}

		return TResult<FAddWidgetToViewportParams>::Success(MoveTemp(Params));
	}

	auto FInputActionParams::FromJson(const TSharedPtr<FJsonObject>& Json) -> TResult<FInputActionParams> {
		if (!Json.IsValid()) {
			return TResult<FInputActionParams>::Failure(TEXT("Invalid JSON object"));
		}

		FInputActionParams Params;

		// Required fields
		if (!Json->TryGetStringField(TEXT("name"), Params.Name)) {
			return TResult<FInputActionParams>::Failure(TEXT("Missing 'name' parameter"));
		}

		// Optional fields with defaults
		Json->TryGetStringField(TEXT("value_type"), Params.ValueType);

		FString Path;
		if (Json->TryGetStringField(TEXT("path"), Path)) {
			Params.Path = Path;
		}

		return TResult<FInputActionParams>::Success(MoveTemp(Params));
	}

	auto FInputMappingContextParams::FromJson(const TSharedPtr<FJsonObject>& Json) -> TResult<FInputMappingContextParams> {
		if (!Json.IsValid()) {
			return TResult<FInputMappingContextParams>::Failure(TEXT("Invalid JSON object"));
		}

		FInputMappingContextParams Params;

		// Required fields
		if (!Json->TryGetStringField(TEXT("name"), Params.Name)) {
			return TResult<FInputMappingContextParams>::Failure(TEXT("Missing 'name' parameter"));
		}

		// Optional fields with defaults
		FString Path;
		if (Json->TryGetStringField(TEXT("path"), Path)) {
			Params.Path = Path;
		}

		return TResult<FInputMappingContextParams>::Success(MoveTemp(Params));
	}

	auto FAddMappingParams::FromJson(const TSharedPtr<FJsonObject>& Json) -> TResult<FAddMappingParams> {
		if (!Json.IsValid()) {
			return TResult<FAddMappingParams>::Failure(TEXT("Invalid JSON object"));
		}

		FAddMappingParams Params;

		// Required fields
		if (!Json->TryGetStringField(TEXT("context_path"), Params.ContextPath)) {
			return TResult<FAddMappingParams>::Failure(TEXT("Missing 'context_path' parameter"));
		}

		if (!Json->TryGetStringField(TEXT("action_path"), Params.ActionPath)) {
			return TResult<FAddMappingParams>::Failure(TEXT("Missing 'action_path' parameter"));
		}

		if (!Json->TryGetStringField(TEXT("key"), Params.Key)) {
			return TResult<FAddMappingParams>::Failure(TEXT("Missing 'key' parameter"));
		}

		return TResult<FAddMappingParams>::Success(MoveTemp(Params));
	}

	auto FStaticMeshParams::FromJson(const TSharedPtr<FJsonObject>& Json) -> TResult<FStaticMeshParams> {
		if (!Json.IsValid()) {
			return TResult<FStaticMeshParams>::Failure(TEXT("Invalid JSON object"));
		}

		FStaticMeshParams Params;

		// Required fields
		if (!Json->TryGetStringField(TEXT("blueprint_name"), Params.BlueprintName)) {
			return TResult<FStaticMeshParams>::Failure(TEXT("Missing 'blueprint_name' parameter"));
		}

		if (!Json->TryGetStringField(TEXT("component_name"), Params.ComponentName)) {
			return TResult<FStaticMeshParams>::Failure(TEXT("Missing 'component_name' parameter"));
		}

		// Optional fields
		FString StaticMesh;
		if (Json->TryGetStringField(TEXT("static_mesh"), StaticMesh)) {
			Params.StaticMesh = StaticMesh;
		}

		FString Material;
		if (Json->TryGetStringField(TEXT("material"), Material)) {
			Params.Material = Material;
		}

		return TResult<FStaticMeshParams>::Success(MoveTemp(Params));
	}

	auto FApplyMappingContextParams::FromJson(const TSharedPtr<FJsonObject>& Json) -> TResult<FApplyMappingContextParams> {
		if (!Json.IsValid()) {
			return TResult<FApplyMappingContextParams>::Failure(TEXT("Invalid JSON object"));
		}

		FApplyMappingContextParams Params;

		// Required fields
		if (!Json->TryGetStringField(TEXT("context_path"), Params.ContextPath)) {
			return TResult<FApplyMappingContextParams>::Failure(TEXT("Missing 'context_path' parameter"));
		}

		// Optional fields with defaults
		if (Json->HasField(TEXT("priority"))) {
			Params.Priority = static_cast<int32>(Json->GetNumberField(TEXT("priority")));
		}

		return TResult<FApplyMappingContextParams>::Success(MoveTemp(Params));
	}

	auto FRemoveMappingContextParams::FromJson(const TSharedPtr<FJsonObject>& Json) -> TResult<FRemoveMappingContextParams> {
		if (!Json.IsValid()) {
			return TResult<FRemoveMappingContextParams>::Failure(TEXT("Invalid JSON object"));
		}

		FRemoveMappingContextParams Params;

		// Required fields
		if (!Json->TryGetStringField(TEXT("context_path"), Params.ContextPath)) {
			return TResult<FRemoveMappingContextParams>::Failure(TEXT("Missing 'context_path' parameter"));
		}

		return TResult<FRemoveMappingContextParams>::Success(MoveTemp(Params));
	}

	auto FLegacyInputMappingParams::FromJson(const TSharedPtr<FJsonObject>& Json) -> TResult<FLegacyInputMappingParams> {
		if (!Json.IsValid()) {
			return TResult<FLegacyInputMappingParams>::Failure(TEXT("Invalid JSON object"));
		}

		FLegacyInputMappingParams Params;

		// Required fields
		if (!Json->TryGetStringField(TEXT("action_name"), Params.ActionName)) {
			return TResult<FLegacyInputMappingParams>::Failure(TEXT("Missing 'action_name' parameter"));
		}

		if (!Json->TryGetStringField(TEXT("key"), Params.Key)) {
			return TResult<FLegacyInputMappingParams>::Failure(TEXT("Missing 'key' parameter"));
		}

		// Optional modifier fields
		if (Json->HasField(TEXT("shift"))) {
			Params.bShift = Json->GetBoolField(TEXT("shift"));
		}
		if (Json->HasField(TEXT("ctrl"))) {
			Params.bCtrl = Json->GetBoolField(TEXT("ctrl"));
		}
		if (Json->HasField(TEXT("alt"))) {
			Params.bAlt = Json->GetBoolField(TEXT("alt"));
		}
		if (Json->HasField(TEXT("cmd"))) {
			Params.bCmd = Json->GetBoolField(TEXT("cmd"));
		}

		return TResult<FLegacyInputMappingParams>::Success(MoveTemp(Params));
	}
}
