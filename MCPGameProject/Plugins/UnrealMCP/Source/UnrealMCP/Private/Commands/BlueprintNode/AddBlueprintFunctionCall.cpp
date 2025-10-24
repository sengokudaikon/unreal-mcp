#include "Commands/BlueprintNode/AddBlueprintFunctionCall.h"
#include "Commands/CommonUtils.h"
#include "Engine/Blueprint.h"
#include "Engine/BlueprintGeneratedClass.h"
#include "EdGraph/EdGraph.h"
#include "EdGraph/EdGraphPin.h"
#include "K2Node_CallFunction.h"
#include "EdGraphSchema_K2.h"
#include "Kismet2/BlueprintEditorUtils.h"
#include "Camera/CameraActor.h"
#include "Kismet/GameplayStatics.h"

// Declare the log category
DEFINE_LOG_CATEGORY_STATIC(LogUnrealMCP, Log, All);
auto FAddBlueprintFunctionCall::Handle(
	const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject> {
	// Get required parameters
	FString BlueprintName;
	if (!Params->TryGetStringField(TEXT("blueprint_name"), BlueprintName)) {
		return FCommonUtils::CreateErrorResponse(TEXT("Missing 'blueprint_name' parameter"));
	}

	FString FunctionName;
	if (!Params->TryGetStringField(TEXT("function_name"), FunctionName)) {
		return FCommonUtils::CreateErrorResponse(TEXT("Missing 'function_name' parameter"));
	}

	// Get position parameters (optional)
	FVector2D NodePosition(0.0f, 0.0f);
	if (Params->HasField(TEXT("node_position"))) {
		NodePosition = FCommonUtils::GetVector2DFromJson(Params, TEXT("node_position"));
	}

	// Check for target parameter (optional)
	FString Target;
	Params->TryGetStringField(TEXT("target"), Target);

	// Find the blueprint
	UBlueprint* Blueprint = FCommonUtils::FindBlueprint(BlueprintName);
	if (!Blueprint) {
		return FCommonUtils::CreateErrorResponse(
			FString::Printf(TEXT("Blueprint not found: %s"), *BlueprintName));
	}

	// Get the event graph
	UEdGraph* EventGraph = FCommonUtils::FindOrCreateEventGraph(Blueprint);
	if (!EventGraph) {
		return FCommonUtils::CreateErrorResponse(TEXT("Failed to get event graph"));
	}

	// Find the function
	UFunction* Function = nullptr;
	UK2Node_CallFunction* FunctionNode = nullptr;

	// Add extensive logging for debugging
	UE_LOG(LogTemp,
	       Display,
	       TEXT("Looking for function '%s' in target '%s'"),
	       *FunctionName,
	       Target.IsEmpty() ? TEXT("Blueprint") : *Target);

	// Check if we have a target class specified
	if (!Target.IsEmpty()) {
		// Try to find the target class
		UClass* TargetClass = nullptr;

		// First try without a prefix
		TargetClass = FindFirstObject<UClass>(*Target, EFindFirstObjectOptions::NativeFirst);
		UE_LOG(LogTemp,
		       Display,
		       TEXT("Tried to find class '%s': %s"),
		       *Target,
		       TargetClass ? TEXT("Found") : TEXT("Not found"));

		// If not found, try with U prefix (common convention for UE classes)
		if (!TargetClass && !Target.StartsWith(TEXT("U"))) {
			FString TargetWithPrefix = FString(TEXT("U")) + Target;
			TargetClass = FindFirstObject<UClass>(*TargetWithPrefix, EFindFirstObjectOptions::NativeFirst);
			UE_LOG(LogTemp,
			       Display,
			       TEXT("Tried to find class '%s': %s"),
			       *TargetWithPrefix,
			       TargetClass ? TEXT("Found") : TEXT("Not found"));
		}

		// If still not found, try with common component names
		if (!TargetClass) {
			// Try some common component class names
			TArray<FString> PossibleClassNames;
			PossibleClassNames.Add(FString(TEXT("U")) + Target + TEXT("Component"));
			PossibleClassNames.Add(Target + TEXT("Component"));

			for (const FString& ClassName : PossibleClassNames) {
				TargetClass = FindFirstObject<UClass>(*ClassName, EFindFirstObjectOptions::NativeFirst);
				if (TargetClass) {
					UE_LOG(LogTemp, Display, TEXT("Found class using alternative name '%s'"), *ClassName);
					break;
				}
			}
		}

		// Special case handling for common classes like UGameplayStatics
		if (!TargetClass && Target == TEXT("UGameplayStatics")) {
			// For UGameplayStatics, use a direct reference to known class
			TargetClass = FindFirstObject<UClass>(TEXT("UGameplayStatics"), EFindFirstObjectOptions::NativeFirst);
			if (!TargetClass) {
				// Try loading it from its known package
				TargetClass = LoadObject<UClass>(nullptr, TEXT("/Script/Engine.GameplayStatics"));
				UE_LOG(LogTemp,
				       Display,
				       TEXT("Explicitly loading GameplayStatics: %s"),
				       TargetClass ? TEXT("Success") : TEXT("Failed"));
			}
		}

		// If we found a target class, look for the function there
		if (TargetClass) {
			UE_LOG(LogTemp,
			       Display,
			       TEXT("Looking for function '%s' in class '%s'"),
			       *FunctionName,
			       *TargetClass->GetName());

			// First try exact name
			Function = TargetClass->FindFunctionByName(*FunctionName);

			// If not found, try class hierarchy
			UClass* CurrentClass = TargetClass;
			while (!Function && CurrentClass) {
				UE_LOG(LogTemp, Display, TEXT("Searching in class: %s"), *CurrentClass->GetName());

				// Try exact match
				Function = CurrentClass->FindFunctionByName(*FunctionName);

				// Try case-insensitive match
				if (!Function) {
					for (TFieldIterator<UFunction> FuncIt(CurrentClass); FuncIt; ++FuncIt) {
						UFunction* AvailableFunc = *FuncIt;
						UE_LOG(LogTemp, Display, TEXT("  - Available function: %s"), *AvailableFunc->GetName());

						if (AvailableFunc->GetName().Equals(FunctionName, ESearchCase::IgnoreCase)) {
							UE_LOG(LogTemp,
							       Display,
							       TEXT("  - Found case-insensitive match: %s"),
							       *AvailableFunc->GetName());
							Function = AvailableFunc;
							break;
						}
					}
				}

				// Move to parent class
				CurrentClass = CurrentClass->GetSuperClass();
			}

			// Special handling for known functions
			if (!Function) {
				if (TargetClass->GetName() == TEXT("GameplayStatics") &&
					(FunctionName == TEXT("GetActorOfClass") || FunctionName.Equals(
						TEXT("GetActorOfClass"),
						ESearchCase::IgnoreCase))) {
					UE_LOG(LogTemp, Display, TEXT("Using special case handling for GameplayStatics::GetActorOfClass"));

					// Create the function node directly
					FunctionNode = NewObject<UK2Node_CallFunction>(EventGraph);
					if (FunctionNode) {
						// Direct setup for known function
						FunctionNode->FunctionReference.SetExternalMember(
							FName(TEXT("GetActorOfClass")),
							TargetClass
						);

						FunctionNode->NodePosX = NodePosition.X;
						FunctionNode->NodePosY = NodePosition.Y;
						EventGraph->AddNode(FunctionNode);
						FunctionNode->CreateNewGuid();
						FunctionNode->PostPlacedNewNode();
						FunctionNode->AllocateDefaultPins();

						UE_LOG(LogTemp, Display, TEXT("Created GetActorOfClass node directly"));

						// List all pins
						for (UEdGraphPin* Pin : FunctionNode->Pins) {
							UE_LOG(LogTemp,
							       Display,
							       TEXT("  - Pin: %s, Direction: %d, Category: %s"),
							       *Pin->PinName.ToString(),
							       (int32)Pin->Direction,
							       *Pin->PinType.PinCategory.ToString());
						}
					}
				}
			}
		}
	}

	// If we still haven't found the function, try in the blueprint's class
	if (!Function && !FunctionNode) {
		UE_LOG(LogTemp, Display, TEXT("Trying to find function in blueprint class"));
		Function = Blueprint->GeneratedClass->FindFunctionByName(*FunctionName);
	}

	// Create the function call node if we found the function
	if (Function && !FunctionNode) {
		FunctionNode = FCommonUtils::CreateFunctionCallNode(EventGraph, Function, NodePosition);
	}

	if (!FunctionNode) {
		return FCommonUtils::CreateErrorResponse(FString::Printf(
			TEXT("Function not found: %s in target %s"),
			*FunctionName,
			Target.IsEmpty() ? TEXT("Blueprint") : *Target));
	}

	// Set parameters if provided
	if (Params->HasField(TEXT("params"))) {
		const TSharedPtr<FJsonObject>* ParamsObj;
		if (Params->TryGetObjectField(TEXT("params"), ParamsObj)) {
			// Process parameters
			for (const TPair<FString, TSharedPtr<FJsonValue>>& Param : (*ParamsObj)->Values) {
				const FString& ParamName = Param.Key;
				const TSharedPtr<FJsonValue>& ParamValue = Param.Value;

				// Find the parameter pin
				UEdGraphPin* ParamPin = FCommonUtils::FindPin(FunctionNode, ParamName, EGPD_Input);
				if (ParamPin) {
					UE_LOG(LogTemp,
					       Display,
					       TEXT("Found parameter pin '%s' of category '%s'"),
					       *ParamName,
					       *ParamPin->PinType.PinCategory.ToString());
					UE_LOG(LogTemp, Display, TEXT("  Current default value: '%s'"), *ParamPin->DefaultValue);
					if (ParamPin->PinType.PinSubCategoryObject.IsValid()) {
						UE_LOG(LogTemp,
						       Display,
						       TEXT("  Pin subcategory: '%s'"),
						       *ParamPin->PinType.PinSubCategoryObject->GetName());
					}

					// Set parameter based on type
					if (ParamValue->Type == EJson::String) {
						FString StringVal = ParamValue->AsString();
						UE_LOG(LogTemp,
						       Display,
						       TEXT("  Setting string parameter '%s' to: '%s'"),
						       *ParamName,
						       *StringVal);

						// Handle class reference parameters (e.g., ActorClass in GetActorOfClass)
						if (ParamPin->PinType.PinCategory == UEdGraphSchema_K2::PC_Class) {
							// For class references, we require the exact class name with proper prefix
							// - Actor classes must start with 'A' (e.g., ACameraActor)
							// - Non-actor classes must start with 'U' (e.g., UObject)
							const FString& ClassName = StringVal;

							// Updated for UE 5.6+ - use FindFirstObject instead of FindObject
							UClass* Class = FindFirstObject<UClass>(*ClassName, EFindFirstObjectOptions::NativeFirst);

							if (!Class) {
								Class = LoadObject<UClass>(nullptr, *ClassName);
								UE_LOG(LogUnrealMCP,
								       Display,
								       TEXT("FindFirstObject<UClass> failed. Assuming soft path  path: %s"),
								       *ClassName);
							}

							// If not found, try with Engine module path
							if (!Class) {
								FString EngineClassName = FString::Printf(TEXT("/Script/Engine.%s"), *ClassName);
								Class = LoadObject<UClass>(nullptr, *EngineClassName);
								UE_LOG(LogUnrealMCP, Display, TEXT("Trying Engine module path: %s"), *EngineClassName);
							}

							if (!Class) {
								UE_LOG(LogUnrealMCP,
								       Error,
								       TEXT(
									       "Failed to find class '%s'. Make sure to use the exact class name with proper prefix (A for actors, U for non-actors)"
								       ),
								       *ClassName);
								return FCommonUtils::CreateErrorResponse(
									FString::Printf(TEXT("Failed to find class '%s'"), *ClassName));
							}

							const UEdGraphSchema_K2* K2Schema = Cast<const UEdGraphSchema_K2>(EventGraph->GetSchema());
							if (!K2Schema) {
								UE_LOG(LogUnrealMCP, Error, TEXT("Failed to get K2Schema"));
								return FCommonUtils::CreateErrorResponse(TEXT("Failed to get K2Schema"));
							}

							K2Schema->TrySetDefaultObject(*ParamPin, Class);
							if (ParamPin->DefaultObject != Class) {
								UE_LOG(LogUnrealMCP,
								       Error,
								       TEXT("Failed to set class reference for pin '%s' to '%s'"),
								       *ParamPin->PinName.ToString(),
								       *ClassName);
								return FCommonUtils::CreateErrorResponse(
									FString::Printf(
										TEXT("Failed to set class reference for pin '%s'"),
										*ParamPin->PinName.ToString()));
							}

							UE_LOG(LogUnrealMCP,
							       Log,
							       TEXT("Successfully set class reference for pin '%s' to '%s'"),
							       *ParamPin->PinName.ToString(),
							       *ClassName);
							continue;
						}
						else if (ParamPin->PinType.PinCategory == UEdGraphSchema_K2::PC_Int) {
							// Ensure we're using an integer value (no decimal)
							int32 IntValue = FMath::RoundToInt(ParamValue->AsNumber());
							ParamPin->DefaultValue = FString::FromInt(IntValue);
							UE_LOG(LogTemp,
							       Display,
							       TEXT("  Set integer parameter '%s' to: %d (string: '%s')"),
							       *ParamName,
							       IntValue,
							       *ParamPin->DefaultValue);
						}
						else if (ParamPin->PinType.PinCategory == UEdGraphSchema_K2::PC_Float) {
							// For other numeric types
							float FloatValue = ParamValue->AsNumber();
							ParamPin->DefaultValue = FString::SanitizeFloat(FloatValue);
							UE_LOG(LogTemp,
							       Display,
							       TEXT("  Set float parameter '%s' to: %f (string: '%s')"),
							       *ParamName,
							       FloatValue,
							       *ParamPin->DefaultValue);
						}
						else if (ParamPin->PinType.PinCategory == UEdGraphSchema_K2::PC_Boolean) {
							bool BoolValue = ParamValue->AsBool();
							ParamPin->DefaultValue = BoolValue ? TEXT("true") : TEXT("false");
							UE_LOG(LogTemp,
							       Display,
							       TEXT("  Set boolean parameter '%s' to: %s"),
							       *ParamName,
							       *ParamPin->DefaultValue);
						}
						else if (ParamPin->PinType.PinCategory == UEdGraphSchema_K2::PC_Struct && ParamPin->PinType.
							PinSubCategoryObject == TBaseStructure<FVector>::Get()) {
							// Handle array parameters - like Vector parameters
							const TArray<TSharedPtr<FJsonValue>>* ArrayValue;
							if (ParamValue->TryGetArray(ArrayValue)) {
								// Check if this could be a vector (array of 3 numbers)
								if (ArrayValue->Num() == 3) {
									// Create a proper vector string: (X=0.0,Y=0.0,Z=1000.0)
									float X = (*ArrayValue)[0]->AsNumber();
									float Y = (*ArrayValue)[1]->AsNumber();
									float Z = (*ArrayValue)[2]->AsNumber();

									FString VectorString = FString::Printf(TEXT("(X=%f,Y=%f,Z=%f)"), X, Y, Z);
									ParamPin->DefaultValue = VectorString;

									UE_LOG(LogTemp,
									       Display,
									       TEXT("  Set vector parameter '%s' to: %s"),
									       *ParamName,
									       *VectorString);
									UE_LOG(LogTemp,
									       Display,
									       TEXT("  Final pin value: '%s'"),
									       *ParamPin->DefaultValue);
								}
								else {
									UE_LOG(LogTemp, Warning, TEXT("Array parameter type not fully supported yet"));
								}
							}
						}
					}
					else if (ParamValue->Type == EJson::Number) {
						// Handle integer vs float parameters correctly
						if (ParamPin->PinType.PinCategory == UEdGraphSchema_K2::PC_Int) {
							// Ensure we're using an integer value (no decimal)
							int32 IntValue = FMath::RoundToInt(ParamValue->AsNumber());
							ParamPin->DefaultValue = FString::FromInt(IntValue);
							UE_LOG(LogTemp,
							       Display,
							       TEXT("  Set integer parameter '%s' to: %d (string: '%s')"),
							       *ParamName,
							       IntValue,
							       *ParamPin->DefaultValue);
						}
						else {
							// For other numeric types
							float FloatValue = ParamValue->AsNumber();
							ParamPin->DefaultValue = FString::SanitizeFloat(FloatValue);
							UE_LOG(LogTemp,
							       Display,
							       TEXT("  Set float parameter '%s' to: %f (string: '%s')"),
							       *ParamName,
							       FloatValue,
							       *ParamPin->DefaultValue);
						}
					}
					else if (ParamValue->Type == EJson::Boolean) {
						bool BoolValue = ParamValue->AsBool();
						ParamPin->DefaultValue = BoolValue ? TEXT("true") : TEXT("false");
						UE_LOG(LogTemp,
						       Display,
						       TEXT("  Set boolean parameter '%s' to: %s"),
						       *ParamName,
						       *ParamPin->DefaultValue);
					}
					else if (ParamValue->Type == EJson::Array) {
						UE_LOG(LogTemp, Display, TEXT("  Processing array parameter '%s'"), *ParamName);
						// Handle array parameters - like Vector parameters
						const TArray<TSharedPtr<FJsonValue>>* ArrayValue;
						if (ParamValue->TryGetArray(ArrayValue)) {
							// Check if this could be a vector (array of 3 numbers)
							if (ArrayValue->Num() == 3 &&
								(ParamPin->PinType.PinCategory == UEdGraphSchema_K2::PC_Struct) &&
								(ParamPin->PinType.PinSubCategoryObject == TBaseStructure<FVector>::Get())) {
								// Create a proper vector string: (X=0.0,Y=0.0,Z=1000.0)
								float X = (*ArrayValue)[0]->AsNumber();
								float Y = (*ArrayValue)[1]->AsNumber();
								float Z = (*ArrayValue)[2]->AsNumber();

								FString VectorString = FString::Printf(TEXT("(X=%f,Y=%f,Z=%f)"), X, Y, Z);
								ParamPin->DefaultValue = VectorString;

								UE_LOG(LogTemp,
								       Display,
								       TEXT("  Set vector parameter '%s' to: %s"),
								       *ParamName,
								       *VectorString);
								UE_LOG(LogTemp,
								       Display,
								       TEXT("  Final pin value: '%s'"),
								       *ParamPin->DefaultValue);
							}
							else {
								UE_LOG(LogTemp, Warning, TEXT("Array parameter type not fully supported yet"));
							}
						}
					}
					// Add handling for other types as needed
				}
				else {
					UE_LOG(LogTemp, Warning, TEXT("Parameter pin '%s' not found"), *ParamName);
				}
			}
		}
	}

	// Mark the blueprint as modified
	FBlueprintEditorUtils::MarkBlueprintAsModified(Blueprint);

	TSharedPtr<FJsonObject> ResultObj = MakeShared<FJsonObject>();
	ResultObj->SetStringField(TEXT("node_id"), FunctionNode->NodeGuid.ToString());
	return ResultObj;
}
