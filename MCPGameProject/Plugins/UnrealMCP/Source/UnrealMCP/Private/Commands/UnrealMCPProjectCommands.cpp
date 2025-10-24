#include "Commands/UnrealMCPProjectCommands.h"
#include "Commands/UnrealMCPCommonUtils.h"
#include "GameFramework/InputSettings.h"
#include "InputAction.h"
#include "InputMappingContext.h"
#include "EnhancedInputSubsystems.h"
#include "EnhancedInputComponent.h"
#include "AssetRegistry/AssetRegistryModule.h"
#include "UObject/SavePackage.h"
#include "Misc/Paths.h"
#include "PackageTools.h"
#include "GameFramework/PlayerController.h"
#include "Engine/World.h"
#include "Editor.h"

FUnrealMCPProjectCommands::FUnrealMCPProjectCommands()
{
}

TSharedPtr<FJsonObject> FUnrealMCPProjectCommands::HandleCommand(const FString& CommandType, const TSharedPtr<FJsonObject>& Params)
{
    // Legacy input commands
    if (CommandType == TEXT("create_input_mapping"))
    {
        return HandleCreateInputMapping(Params);
    }

    // Enhanced Input commands
    if (CommandType == TEXT("create_enhanced_input_action"))
    {
        return HandleCreateEnhancedInputAction(Params);
    }
    if (CommandType == TEXT("create_input_mapping_context"))
    {
        return HandleCreateInputMappingContext(Params);
    }
    if (CommandType == TEXT("add_enhanced_input_mapping"))
    {
        return HandleAddEnhancedInputMapping(Params);
    }
    if (CommandType == TEXT("remove_enhanced_input_mapping"))
    {
        return HandleRemoveEnhancedInputMapping(Params);
    }
    if (CommandType == TEXT("apply_mapping_context"))
    {
        return HandleApplyMappingContext(Params);
    }
    if (CommandType == TEXT("remove_mapping_context"))
    {
        return HandleRemoveMappingContext(Params);
    }
    if (CommandType == TEXT("clear_all_mapping_contexts"))
    {
        return HandleClearAllMappingContexts(Params);
    }

    return FUnrealMCPCommonUtils::CreateErrorResponse(FString::Printf(TEXT("Unknown project command: %s"), *CommandType));
}

TSharedPtr<FJsonObject> FUnrealMCPProjectCommands::HandleCreateInputMapping(const TSharedPtr<FJsonObject>& Params)
{
    // Get required parameters
    FString ActionName;
    if (!Params->TryGetStringField(TEXT("action_name"), ActionName))
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Missing 'action_name' parameter"));
    }

    FString Key;
    if (!Params->TryGetStringField(TEXT("key"), Key))
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Missing 'key' parameter"));
    }

    // Get the input settings
    UInputSettings* InputSettings = GetMutableDefault<UInputSettings>();
    if (!InputSettings)
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Failed to get input settings"));
    }

    // Create the input action mapping
    FInputActionKeyMapping ActionMapping;
    ActionMapping.ActionName = FName(*ActionName);
    ActionMapping.Key = FKey(*Key);

    // Add modifiers if provided
    if (Params->HasField(TEXT("shift")))
    {
        ActionMapping.bShift = Params->GetBoolField(TEXT("shift"));
    }
    if (Params->HasField(TEXT("ctrl")))
    {
        ActionMapping.bCtrl = Params->GetBoolField(TEXT("ctrl"));
    }
    if (Params->HasField(TEXT("alt")))
    {
        ActionMapping.bAlt = Params->GetBoolField(TEXT("alt"));
    }
    if (Params->HasField(TEXT("cmd")))
    {
        ActionMapping.bCmd = Params->GetBoolField(TEXT("cmd"));
    }

    // Add the mapping
    InputSettings->AddActionMapping(ActionMapping);
    InputSettings->SaveConfig();

    TSharedPtr<FJsonObject> ResultObj = MakeShared<FJsonObject>();
    ResultObj->SetStringField(TEXT("action_name"), ActionName);
    ResultObj->SetStringField(TEXT("key"), Key);
    return ResultObj;
}

// ========================================
// Enhanced Input Command Handlers
// ========================================

TSharedPtr<FJsonObject> FUnrealMCPProjectCommands::HandleCreateEnhancedInputAction(const TSharedPtr<FJsonObject>& Params)
{
    // Get required parameters
    FString ActionName;
    if (!Params->TryGetStringField(TEXT("name"), ActionName))
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Missing 'name' parameter"));
    }

    FString ValueTypeStr;
    if (!Params->TryGetStringField(TEXT("value_type"), ValueTypeStr))
    {
        ValueTypeStr = TEXT("Boolean"); // Default to Boolean
    }

    FString AssetPath;
    if (!Params->TryGetStringField(TEXT("path"), AssetPath))
    {
        AssetPath = TEXT("/Game/Input"); // Default path
    }

    // Map value type string to enum
    EInputActionValueType ValueType = EInputActionValueType::Boolean;
    if (ValueTypeStr == TEXT("Axis1D"))
    {
        ValueType = EInputActionValueType::Axis1D;
    }
    else if (ValueTypeStr == TEXT("Axis2D"))
    {
        ValueType = EInputActionValueType::Axis2D;
    }
    else if (ValueTypeStr == TEXT("Axis3D"))
    {
        ValueType = EInputActionValueType::Axis3D;
    }

    // Create package path
    FString PackagePath = AssetPath / FString::Printf(TEXT("IA_%s"), *ActionName);
    UPackage* Package = CreatePackage(*PackagePath);
    if (!Package)
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Failed to create package"));
    }

    // Create the Input Action asset
    UInputAction* InputAction = NewObject<UInputAction>(Package, *FString::Printf(TEXT("IA_%s"), *ActionName), RF_Public | RF_Standalone);
    if (!InputAction)
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Failed to create Input Action"));
    }

    InputAction->ValueType = ValueType;

    // Mark package as dirty and save
    Package->MarkPackageDirty();
    FAssetRegistryModule::AssetCreated(InputAction);

    // Save the asset
    FString PackageFileName = FPackageName::LongPackageNameToFilename(PackagePath, FPackageName::GetAssetPackageExtension());
    FSavePackageArgs SaveArgs;
    SaveArgs.TopLevelFlags = RF_Public | RF_Standalone;
    SaveArgs.SaveFlags = SAVE_NoError;

    if (!UPackage::SavePackage(Package, InputAction, *PackageFileName, SaveArgs))
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Failed to save Input Action asset"));
    }

    TSharedPtr<FJsonObject> ResultObj = MakeShared<FJsonObject>();
    ResultObj->SetStringField(TEXT("name"), ActionName);
    ResultObj->SetStringField(TEXT("value_type"), ValueTypeStr);
    ResultObj->SetStringField(TEXT("asset_path"), PackagePath);
    return ResultObj;
}

TSharedPtr<FJsonObject> FUnrealMCPProjectCommands::HandleCreateInputMappingContext(const TSharedPtr<FJsonObject>& Params)
{
    // Get required parameters
    FString ContextName;
    if (!Params->TryGetStringField(TEXT("name"), ContextName))
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Missing 'name' parameter"));
    }

    FString AssetPath;
    if (!Params->TryGetStringField(TEXT("path"), AssetPath))
    {
        AssetPath = TEXT("/Game/Input"); // Default path
    }

    // Create package path
    FString PackagePath = AssetPath / FString::Printf(TEXT("IMC_%s"), *ContextName);
    UPackage* Package = CreatePackage(*PackagePath);
    if (!Package)
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Failed to create package"));
    }

    // Create the Input Mapping Context asset
    UInputMappingContext* MappingContext = NewObject<UInputMappingContext>(Package, *FString::Printf(TEXT("IMC_%s"), *ContextName), RF_Public | RF_Standalone);
    if (!MappingContext)
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Failed to create Input Mapping Context"));
    }

    // Mark package as dirty and save
    Package->MarkPackageDirty();
    FAssetRegistryModule::AssetCreated(MappingContext);

    // Save the asset
    FString PackageFileName = FPackageName::LongPackageNameToFilename(PackagePath, FPackageName::GetAssetPackageExtension());
    FSavePackageArgs SaveArgs;
    SaveArgs.TopLevelFlags = RF_Public | RF_Standalone;
    SaveArgs.SaveFlags = SAVE_NoError;

    if (!UPackage::SavePackage(Package, MappingContext, *PackageFileName, SaveArgs))
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Failed to save Input Mapping Context asset"));
    }

    TSharedPtr<FJsonObject> ResultObj = MakeShared<FJsonObject>();
    ResultObj->SetStringField(TEXT("name"), ContextName);
    ResultObj->SetStringField(TEXT("asset_path"), PackagePath);
    return ResultObj;
}

TSharedPtr<FJsonObject> FUnrealMCPProjectCommands::HandleAddEnhancedInputMapping(const TSharedPtr<FJsonObject>& Params)
{
    // Get required parameters
    FString ContextPath;
    if (!Params->TryGetStringField(TEXT("context_path"), ContextPath))
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Missing 'context_path' parameter"));
    }

    FString ActionPath;
    if (!Params->TryGetStringField(TEXT("action_path"), ActionPath))
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Missing 'action_path' parameter"));
    }

    FString Key;
    if (!Params->TryGetStringField(TEXT("key"), Key))
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Missing 'key' parameter"));
    }

    // Load the Input Mapping Context
    UInputMappingContext* MappingContext = LoadObject<UInputMappingContext>(nullptr, *ContextPath);
    if (!MappingContext)
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(FString::Printf(TEXT("Failed to load Input Mapping Context: %s"), *ContextPath));
    }

    // Load the Input Action
    UInputAction* InputAction = LoadObject<UInputAction>(nullptr, *ActionPath);
    if (!InputAction)
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(FString::Printf(TEXT("Failed to load Input Action: %s"), *ActionPath));
    }

    // Create the key mapping
    FEnhancedActionKeyMapping& Mapping = MappingContext->MapKey(InputAction, FKey(*Key));

    // TODO: Add support for modifiers and triggers
    // This can be expanded later to support:
    // - Input Modifiers (Negate, Scalar, DeadZone, etc.)
    // - Input Triggers (Pressed, Released, Hold, Tap, etc.)

    // Mark the asset as modified
    MappingContext->MarkPackageDirty();

    // Save the mapping context
    FString PackageName = MappingContext->GetOutermost()->GetName();
    FString PackageFileName = FPackageName::LongPackageNameToFilename(PackageName, FPackageName::GetAssetPackageExtension());

    FSavePackageArgs SaveArgs;
    SaveArgs.TopLevelFlags = RF_Public | RF_Standalone;
    SaveArgs.SaveFlags = SAVE_NoError;

    if (!UPackage::SavePackage(MappingContext->GetOutermost(), MappingContext, *PackageFileName, SaveArgs))
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Failed to save Input Mapping Context"));
    }

    TSharedPtr<FJsonObject> ResultObj = MakeShared<FJsonObject>();
    ResultObj->SetStringField(TEXT("context_path"), ContextPath);
    ResultObj->SetStringField(TEXT("action_path"), ActionPath);
    ResultObj->SetStringField(TEXT("key"), Key);
    return ResultObj;
}

TSharedPtr<FJsonObject> FUnrealMCPProjectCommands::HandleRemoveEnhancedInputMapping(const TSharedPtr<FJsonObject>& Params)
{
    // Get required parameters
    FString ContextPath;
    if (!Params->TryGetStringField(TEXT("context_path"), ContextPath))
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Missing 'context_path' parameter"));
    }

    FString ActionPath;
    if (!Params->TryGetStringField(TEXT("action_path"), ActionPath))
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Missing 'action_path' parameter"));
    }

    // Load the Input Mapping Context
    UInputMappingContext* MappingContext = LoadObject<UInputMappingContext>(nullptr, *ContextPath);
    if (!MappingContext)
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(FString::Printf(TEXT("Failed to load Input Mapping Context: %s"), *ContextPath));
    }

    // Load the Input Action
    UInputAction* InputAction = LoadObject<UInputAction>(nullptr, *ActionPath);
    if (!InputAction)
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(FString::Printf(TEXT("Failed to load Input Action: %s"), *ActionPath));
    }

    // Remove all mappings for this action
    MappingContext->UnmapKey(InputAction, FKey());

    // Mark the asset as modified and save
    MappingContext->MarkPackageDirty();

    FString PackageName = MappingContext->GetOutermost()->GetName();
    FString PackageFileName = FPackageName::LongPackageNameToFilename(PackageName, FPackageName::GetAssetPackageExtension());

    FSavePackageArgs SaveArgs;
    SaveArgs.TopLevelFlags = RF_Public | RF_Standalone;
    SaveArgs.SaveFlags = SAVE_NoError;

    if (!UPackage::SavePackage(MappingContext->GetOutermost(), MappingContext, *PackageFileName, SaveArgs))
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Failed to save Input Mapping Context"));
    }

    TSharedPtr<FJsonObject> ResultObj = MakeShared<FJsonObject>();
    ResultObj->SetStringField(TEXT("context_path"), ContextPath);
    ResultObj->SetStringField(TEXT("action_path"), ActionPath);
    return ResultObj;
}

TSharedPtr<FJsonObject> FUnrealMCPProjectCommands::HandleApplyMappingContext(const TSharedPtr<FJsonObject>& Params)
{
    // Get required parameters
    FString ContextPath;
    if (!Params->TryGetStringField(TEXT("context_path"), ContextPath))
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Missing 'context_path' parameter"));
    }

    int32 Priority = 0;
    if (Params->HasField(TEXT("priority")))
    {
        Priority = static_cast<int32>(Params->GetNumberField(TEXT("priority")));
    }

    // Load the Input Mapping Context
    UInputMappingContext* MappingContext = LoadObject<UInputMappingContext>(nullptr, *ContextPath);
    if (!MappingContext)
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(FString::Printf(TEXT("Failed to load Input Mapping Context: %s"), *ContextPath));
    }

    // Get the first player controller
    UWorld* World = GEditor ? GEditor->GetEditorWorldContext().World() : nullptr;
    if (!World)
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Failed to get world"));
    }

    APlayerController* PlayerController = World->GetFirstPlayerController();
    if (!PlayerController)
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("No player controller found"));
    }

    // Get the Enhanced Input Local Player Subsystem
    UEnhancedInputLocalPlayerSubsystem* Subsystem = ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(PlayerController->GetLocalPlayer());
    if (!Subsystem)
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Failed to get Enhanced Input Subsystem"));
    }

    // Add the mapping context
    Subsystem->AddMappingContext(MappingContext, Priority);

    TSharedPtr<FJsonObject> ResultObj = MakeShared<FJsonObject>();
    ResultObj->SetStringField(TEXT("context_path"), ContextPath);
    ResultObj->SetNumberField(TEXT("priority"), Priority);
    return ResultObj;
}

TSharedPtr<FJsonObject> FUnrealMCPProjectCommands::HandleRemoveMappingContext(const TSharedPtr<FJsonObject>& Params)
{
    // Get required parameters
    FString ContextPath;
    if (!Params->TryGetStringField(TEXT("context_path"), ContextPath))
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Missing 'context_path' parameter"));
    }

    // Load the Input Mapping Context
    UInputMappingContext* MappingContext = LoadObject<UInputMappingContext>(nullptr, *ContextPath);
    if (!MappingContext)
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(FString::Printf(TEXT("Failed to load Input Mapping Context: %s"), *ContextPath));
    }

    // Get the first player controller
    UWorld* World = GEditor ? GEditor->GetEditorWorldContext().World() : nullptr;
    if (!World)
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Failed to get world"));
    }

    APlayerController* PlayerController = World->GetFirstPlayerController();
    if (!PlayerController)
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("No player controller found"));
    }

    // Get the Enhanced Input Local Player Subsystem
    UEnhancedInputLocalPlayerSubsystem* Subsystem = ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(PlayerController->GetLocalPlayer());
    if (!Subsystem)
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Failed to get Enhanced Input Subsystem"));
    }

    // Remove the mapping context
    Subsystem->RemoveMappingContext(MappingContext);

    TSharedPtr<FJsonObject> ResultObj = MakeShared<FJsonObject>();
    ResultObj->SetStringField(TEXT("context_path"), ContextPath);
    return ResultObj;
}

TSharedPtr<FJsonObject> FUnrealMCPProjectCommands::HandleClearAllMappingContexts(const TSharedPtr<FJsonObject>& Params)
{
    // Get the first player controller
    UWorld* World = GEditor ? GEditor->GetEditorWorldContext().World() : nullptr;
    if (!World)
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Failed to get world"));
    }

    APlayerController* PlayerController = World->GetFirstPlayerController();
    if (!PlayerController)
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("No player controller found"));
    }

    // Get the Enhanced Input Local Player Subsystem
    UEnhancedInputLocalPlayerSubsystem* Subsystem = ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(PlayerController->GetLocalPlayer());
    if (!Subsystem)
    {
        return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Failed to get Enhanced Input Subsystem"));
    }

    // Clear all mapping contexts
    Subsystem->ClearAllMappings();

    TSharedPtr<FJsonObject> ResultObj = MakeShared<FJsonObject>();
    ResultObj->SetBoolField(TEXT("success"), true);
    return ResultObj;
} 