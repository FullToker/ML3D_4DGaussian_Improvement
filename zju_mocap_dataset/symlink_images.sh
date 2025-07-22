#!/bin/bash

# Loop from 1 to 21
for i in $(seq 1 21); do
  # Format target folder: cam01, cam02, ..., cam21
  target=$(printf "cam%02d" $i)

  # Format symlink name: cam_00001, cam_00002, ..., cam_00021
  link_name=$(printf "cam_%05d" $i)

  # Create symbolic link
  ln -sfn "$target" "$link_name"
done

echo "Symlinks created."
