# Re-rendering the hero

The README header is a GIF recorded from a three.js scene, because GitHub won't run JavaScript in a README.

1. `npm install` in this folder.
2. Copy Unitree's G1 model into `g1/`: from [unitree_ros](https://github.com/unitreerobotics/unitree_ros), take `robots/g1_description/g1_29dof_with_hand_rev_1_0.urdf` and the `meshes/` folder.
3. Serve the folder: `python3 -m http.server 8765`
4. Open `http://localhost:8765/index.html` to see it live, or record frames:
   `python3 capture.py http://localhost:8765 frames 36` (needs `pip install playwright`)
5. Encode the loop:
   ```
   ffmpeg -framerate 25 -i frames/f%03d.png -vf "split[a][b];[a]palettegen=max_colors=256:stats_mode=full[p];[b][p]paletteuse=dither=sierra2_4a" -loop 0 ../assets/hero.gif
   ```

Edit the copy in `index.html` (`#copy`). The wave lives in `applyPose()`; the pose and camera defaults can be overridden with URL params such as `?yaw=-1.2&amp=0.4`.
