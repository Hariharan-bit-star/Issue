Notes & advanced ideas

Units: This pawn uses a pragmatic mix of cm (Unreal units) and SI for forces. The forces and coefficients are tuned for good gameplay feel — you can convert to fully SI consistent if you want physical accuracy (multiply positions by 100, etc).

Waves / varying surface: Query a Water actor or a heightmap to compute local WaterLevelZ instead of a single flat plane.

Submersion fraction: Instead of origin-only submersion, compute hull/mesh bounds overlap with water to get a more realistic buoyant force.

Swimming animation: Drive animation blendspace by Velocity.Size() and bSprint, and trigger "breath" animation at surface.

Underwater physics component: Consider creating a UUnderwaterMovementComponent if you plan to reuse across pawns.

Example: use the uploaded map image (if helpful)

If you want to use the previously uploaded world-map image as a texture or level reference, here's its path (you can convert/serve it as needed):

sandbox:/mnt/data/A_Mercator_projection_of_a_world_map_in_the_digita.png

If you want, I can next:

convert this into a MovementComponent (clean separation),

add wave-height sampling to compute local WaterLevelZ,

provide a Blueprint-ready version with camera shakes & VFX,

or tune parameters for a realistic scuba diver vs arcade swimmer feel.