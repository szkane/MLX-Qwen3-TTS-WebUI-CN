# Multi-Person Conversation Voice Source Selection Feature

## Implementation Date
2026-02-24

## Summary
Successfully implemented voice source selection for the multi-person conversation TTS feature. Users can now choose between "Voice Design" (describe voice in natural language) or "Saved Voices" (use previously saved voice clones from the Voice Clone tab) for each speaker in a conversation.

## Bug Fixes (2026-02-24)

### Bug 1: Saved Voice Cleared When Adding New Speaker
**Problem**: When adding a third speaker, the previously selected saved voice was cleared.

**Root Cause**: The `renderConversationSpeakers` function was saving values from hidden panels, which could have empty values.

**Fix**: Only save `instruct` when voice_design panel is active, and only save `prompt_id` when saved_voice panel is active and has a value:

```javascript
// Only save prompt_id when saved_voice panel is active
const savedVoicePanel = card.querySelector('.saved-voice-panel');
const isSavedVoiceActive = savedVoicePanel && savedVoicePanel.style.display !== 'none';
if (promptIdEl && isSavedVoiceActive && promptIdEl.value) {
    state.conversationSpeakers[index].prompt_id = promptIdEl.value;
}
```

### Bug 2: API Documentation Clarity
**Problem**: API docs didn't clarify that `prompt_id` references saved voice data containing `ref_audio_base64` and `ref_text`.

**Fix**: Updated `requestParams` description for `prompt_id`:
> "Saved voice prompt ID to use (required when voice_source is "saved_voice"). The server will use the associated ref_audio_base64 and ref_text from the saved prompt."

## Changes Made

### Backend (server.py)

1. **Updated ConversationSpeaker Model** (lines 194-200):
   ```python
   class ConversationSpeaker(BaseModel):
       text: str
       language: Optional[str] = "Auto"
       voice_source: str = "voice_design"  # "voice_design" or "saved_voice"
       instruct: Optional[str] = None      # For voice_design
       prompt_id: Optional[str] = None     # For saved_voice
   ```

2. **Updated generate_conversation Endpoint** (lines 466-527):
   - Checks `voice_source` for each speaker
   - For `voice_design`: Uses VoiceDesign model with `instruct` parameter
   - For `saved_voice`: Uses Base model with saved voice prompt (ref_audio + ref_text)
   - Creates temporary file for reference audio when using saved voices
   - Properly cleans up temp files after generation

### Frontend JavaScript (static/app.js)

1. **Updated State** (lines 1480-1483):
   - Added `voice_source` field to conversation speakers
   - Added `prompt_id` field for saved voice selection

2. **Updated renderConversationSpeakers Function** (lines 1960-2063):
   - Added Voice Source dropdown (Voice Design / Saved Voices)
   - Added Voice Design panel with instruct textarea
   - Added Saved Voice panel with dropdown of saved voices
   - Panels show/hide based on selected voice source
   - Saves `voice_source` and `prompt_id` values from DOM

3. **Updated addConversationSpeaker Function** (lines 2082-2098):
   - Added `voice_source: 'voice_design'` default
   - Added `prompt_id: ''` default

4. **Updated generateConversation Function** (lines 2114-2155):
   - Collects `voice_source` and `prompt_id` from DOM
   - Validates based on voice source:
     - Voice Design: requires `instruct`
     - Saved Voice: requires `prompt_id`
   - Sends correct data structure to API

5. **Updated initConversationTab Function** (lines 3328-3380):
   - Added `loadSavedPrompts()` call on init
   - Added change event handler for voice source dropdown
   - Toggles panel visibility when voice source changes

6. **New loadSavedPrompts Function** (lines 3382-3396):
   - Fetches saved voices from `/api/v1/base/prompts`
   - Updates `state.savedPrompts`
   - Re-renders conversation speakers to show updated list

### Frontend CSS (static/styles.css)

1. **Added Panel Styles** (lines 2333-2347):
   - `.voice-design-panel`: Cyan left border
   - `.saved-voice-panel`: Amber left border
   - Consistent padding and background

## UI Flow

1. User opens "Multi-Person Conversation" tab
2. Each speaker card shows:
   - Voice Source dropdown (Voice Design / Saved Voices)
   - Voice Design panel (voice description textarea) - shown by default
   - Saved Voice panel (dropdown of saved voices) - hidden by default
3. When user selects "Saved Voices":
   - Voice Design panel hides
   - Saved Voice panel shows with dropdown
   - If no saved voices, shows hint to create one in Voice Clone tab
4. When user selects "Voice Design":
   - Voice Design panel shows
   - Saved Voice panel hides
5. Generation validates based on selected source

## API Specification

### Request
```json
POST /api/v1/conversation/generate
{
  "speakers": [
    {
      "voice_source": "voice_design",
      "text": "Hello!",
      "instruct": "A warm male voice",
      "language": "English"
    },
    {
      "voice_source": "saved_voice",
      "text": "Hi there!",
      "prompt_id": "abc-123-def",
      "language": "English"
    }
  ],
  "speed": 1.0,
  "response_format": "base64"
}
```

## Features

### User Features
- Mix Voice Design and Saved Voices in same conversation
- Real-time panel switching when changing voice source
- Saved voices loaded automatically on tab open
- Validation messages for missing required fields
- Visual distinction between panel types (cyan vs amber borders)

### Technical Features
- Backend handles both voice sources in single endpoint
- Temporary file creation/cleanup for saved voice audio
- Proper error handling for missing prompt_id
- Event delegation for dynamic speaker cards

## Files Modified

| File | Changes |
|------|---------|
| `server.py` | ~70 lines (updated model + endpoint) |
| `static/app.js` | ~150 lines (render + generate + init functions) |
| `static/styles.css` | ~15 lines (panel styles) |

## Verification Steps

1. Start server: `python server.py`
2. Open http://localhost:7860/demo
3. Navigate to "Multi-Person Conversation" tab
4. Verify Voice Source dropdown appears for each speaker
5. Switch between "Voice Design" and "Saved Voices"
6. Verify panels show/hide correctly
7. Create a saved voice in Voice Clone tab first
8. Return to Conversation tab and verify saved voice appears in dropdown
9. Test conversation generation with mixed voice sources

## Future Enhancements

1. Add "Preview" button to hear saved voice sample
2. Add voice categories/tags for better organization
3. Add search/filter for saved voices when list grows large
4. Add "favorite" marker for frequently used voices
5. Add bulk voice source change for all speakers

## Conclusion

The voice source selection feature has been successfully implemented. Users can now combine the flexibility of Voice Design (custom voice descriptions) with the consistency of Saved Voices (previously cloned voices) in multi-person conversations.
