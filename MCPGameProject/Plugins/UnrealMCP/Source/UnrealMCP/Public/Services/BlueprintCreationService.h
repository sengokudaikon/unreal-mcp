#pragma once

#include "CoreMinimal.h"
#include "Core/Result.h"
#include "Core/MCPTypes.h"
#include "Json.h"

class UBlueprint;
class UClass;

namespace UnrealMCP
{
	/**
	 * Service for blueprint creation and compilation operations
	 * Handles the complete lifecycle of blueprint assets from creation to compilation
	 */
	class UNREALMCP_API FBlueprintCreationService
	{
	public:
		/**
		 * Create a new blueprint with the specified parent class
		 * @param Params Configuration for the new blueprint
		 * @return Result containing the created blueprint or an error message
		 */
		static TResult<UBlueprint*> CreateBlueprint(const FBlueprintCreationParams& Params);

		/**
		 * Create a blueprint and return result as JSON
		 * @param Params Configuration for the new blueprint
		 * @return JSON response with blueprint details or error information
		 */
		static TSharedPtr<FJsonObject> CreateBlueprintAsJson(const FBlueprintCreationParams& Params);

		/**
		 * Compile an existing blueprint by name
		 * @param BlueprintName The name of the blueprint to compile
		 * @return Result indicating success or compilation error
		 */
		static FVoidResult CompileBlueprint(const FString& BlueprintName);

		/**
		 * Compile a blueprint and return result as JSON
		 * @param BlueprintName The name of the blueprint to compile
		 * @return JSON response with compilation status or error information
		 */
		static TSharedPtr<FJsonObject> CompileBlueprintAsJson(const FString& BlueprintName);

	private:
		/**
		 * Resolve a parent class name to a UClass instance
		 * Attempts to find the class in Engine or Game modules with fallback to AActor
		 * @param ParentClassName The name of the class (with or without 'A' prefix)
		 * @return Valid UClass pointer, defaults to AActor if not found
		 */
		static UClass* ResolveParentClass(const FString& ParentClassName);

		/**
		 * Helper to create error JSON response
		 */
		static TSharedPtr<FJsonObject> CreateErrorResponse(const FString& Error);

		/**
		 * Helper to create success JSON response
		 */
		static TSharedPtr<FJsonObject> CreateSuccessResponse(const TSharedPtr<FJsonObject>& Data = nullptr);
	};
}
