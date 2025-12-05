{
  description = "DataSet Flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };

  outputs = inputs @ {flake-parts, ...}:
    flake-parts.lib.mkFlake {inherit inputs;} {
      systems = [
        "x86_64-linux"
        "aarch64-linux"
      ];
      perSystem = {pkgs, ...}:
        with pkgs; rec {
          devShells.default = callPackage ./shell.nix {};
          formatter = alejandra;
        };
    };
}

