#pragma once

#include "CoreMinimal.h"
#include "Core/Result.h"
#include "Core/MCPTypes.h"
#include "Json.h"

class UWidgetBlueprint;
class UWidget;
class UTextBlock;
class UButton;
class UCanvasPanelSlot;

namespace UnrealMCP
{
	/**
	 * High-level service for UMG widget operations
	 * Coordinates between widget creation, manipulation, and viewport integration
	 *
	 * All operations return TResult<T> for consistency. JSON conversion is handled
	 * at the command handler layer, not within the service itself.
	 */
	class UNREALMCP_API FWidgetService
	{
	public:
		// Widget creation
		static TResult<UWidgetBlueprint*> CreateWidget(const FWidgetCreationParams& Params);

		// Text block operations
		static TResult<UTextBlock*> AddTextBlock(const FTextBlockParams& Params);

		// Button operations
		static TResult<UButton*> AddButton(const FButtonParams& Params);

		// Event binding
		static FVoidResult BindWidgetEvent(const FWidgetEventBindingParams& Params);

		// Text block binding
		static FVoidResult SetTextBlockBinding(const FTextBlockBindingParams& Params);

		// Viewport integration (returns widget class info, actual viewport addition is done in blueprints)
		static TResult<UClass*> GetWidgetClass(const FAddWidgetToViewportParams& Params);

	private:
		/**
		 * Resolves a widget name to a full asset path
		 * Supports both full paths (e.g., "/Game/UI/MyWidget") and short names (e.g., "MyWidget")
		 * Short names are assumed to be in /Game/UI directory
		 */
		static FString ResolveWidgetPath(const FString& WidgetName);

		/**
		 * Validates that a widget blueprint has a valid Canvas Panel root
		 * Required for adding widgets to the hierarchy
		 */
		static FVoidResult ValidateCanvasRoot(const UWidgetBlueprint* WidgetBlueprint);

		/**
		 * Applies position and size properties to a canvas panel slot if parameters are set
		 */
		static void ApplyCanvasSlotTransform(::UCanvasPanelSlot* Slot, const TOptional<FVector2D>& Position, const TOptional<FVector2D>& Size);
	};
}
