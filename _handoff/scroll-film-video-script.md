# Scroll film as video: shot script

Goal: replace the three.js 3D scroll film on the homepage with real-looking video that scrubs with
scroll, the same way the 3D does now (scroll down plays forward, scroll up plays backward).
Same story, same kit, same chapter copy. Everything is set in the **same house as the hero video**:
the white marble kitchen counter, cream walls, light oak floors, tan linen sofa, walnut wood,
warm morning sun.

Made in Higgsfield **in Claude chat** (free trial unlimited only works there, not in Claude Code).
Use the hero photo (marble counter, tan cloth, glass spray bottle) as the reference image for every
still so the house, light and kit match.

## The story (matches the page copy)

| # | Chapter on the page | What the 3D shows now | Video version |
|---|---|---|---|
| 1 | Hero: "Cleaned to the last detail" | Spray bottle floating, pearl bubbles drifting | Glass spray bottle on the counter, pearly soap bubbles drifting around it |
| 2 | 01 Spray | Bubbles turn into mist from the nozzle | Bottle sprays a fine mist across the marble, droplets catch the sun |
| 3 | 02 Wipe | Microfiber cloth wipes in loops | Tan microfiber cloth glides across the wet marble by itself, leaving a shine |
| 4 | 03 Scrub | Scrub brush scrubs, foam bubbles | Wooden scrub brush scrubs the grout of the backsplash, soft white foam |
| 5 | 04 Check | Bubbles rise away | Spotless counter, the last bubbles float up and pop, everything gleams |
| 6 | Final: "Detail, done right." | Kit lined up, slowly turning | Bottle, folded cloth, sponge and brush lined up on the counter, slow camera arc |

No people and no hands (like the 3D: the tools move on their own). No text, no logos.
Warm neutrals only: white, cream, tan, brown.

## Step A: six stills (GPT Image 2.6, 16:9, 2K, medium)

Every still starts with this line:
> Same kitchen as the reference image: white marble counter, cream walls, light oak floors, tan linen sofa and walnut wood softly out of focus behind, warm morning sunlight. Photorealistic. Only warm neutral colors (white, cream, tan, brown). No people, no hands, no text, no logos.

1. **Hero.** Close-up of the clear glass spray bottle standing on the marble counter, right of center. A few pearly, iridescent-cream soap bubbles float in the air around it, catching the sun. Empty space on the left.
2. **Spray.** The same glass spray bottle tilted slightly, spraying a fine sparkling mist to the left over the marble counter. Tiny droplets glow in the sunlight.
3. **Wipe.** A tan microfiber cloth, gently rippled, gliding across the wet marble counter. Behind it the marble shines streak-free; ahead of it a few water droplets. Spray bottle soft in the background at right.
4. **Scrub.** A wooden scrub brush with cream bristles scrubbing the grout line where the marble counter meets a cream tile backsplash. Soft white foam and small pearly bubbles around the bristles.
5. **Check.** The spotless marble counter gleaming in the sun, reflections crisp. The last few pearly bubbles float upward and away. Calm and finished.
6. **Final.** Cleaning kit neatly lined up on the marble counter: the glass spray bottle, the folded tan microfiber cloth, a tan sponge and the wooden scrub brush. The kitchen and living room behind, softly out of focus. Empty space on the left.

## Step B: five moves between the stills (Seedance 2.0, 16:9, 720p, 5 s, no audio)

Each clip uses still N as the **start image** and still N+1 as the **end image**, so the five clips
join into one continuous film. Every prompt ends with:
> One smooth continuous shot, no cuts. Slow, calm camera. No people, no hands, no text. No audio.

1. Still 1 to 2: The bubbles drift toward the nozzle; the bottle tilts and sprays a fine mist across the marble.
2. Still 2 to 3: The mist settles on the marble; a tan microfiber cloth glides in from the right and wipes it to a shine.
3. Still 3 to 4: The camera follows the cloth to the back of the counter, where a wooden scrub brush scrubs the backsplash grout and foam forms.
4. Still 4 to 5: The brush lifts away, the foam turns into pearly bubbles that rise and pop, leaving the counter gleaming.
5. Still 5 to 6: The camera eases back and slowly arcs as the kit settles into a neat lineup on the counter.

## Step C: Claude Code builds it

Joins the five clips into one film (plus a phone crop or a 9:16 set), encodes it so scrubbing
is smooth both ways, swaps the three.js canvas for the video, and keeps all the chapter copy,
buttons and word-by-word headlines exactly as they are.
