{

  description = "Flake to build the nrich package in this repo, as well as run devShells for it";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-23.05";
    nixpkgs-unstable.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs, nixpkgs-unstable }@inputs:
    let
      inherit (self) outputs;
      forAllSystems = nixpkgs.lib.genAttrs [
        "aarch64-linux"
        "i686-linux"
        "x86_64-linux"
        "aarch64-darwin"
        "x86_64-darwin"
      ];

    in
    {
      packages = forAllSystems(system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in rec {
          nrich = pkgs.callPackage ./nrich.nix { };

          # `nix build` needs default target
          default = nrich;
      });

      # nix fmt
      formatter = forAllSystems (system: nixpkgs.legacyPackages.${system}.nixpkgs-fmt);

      # Accessible through 'nix develop' or 'nix-shell' (legacy)
      devShells = forAllSystems (system:
        let
          pkgs = import nixpkgs {
            inherit system;
            overlays = [
              (final: prev: {
                nrich = pkgs.callPackage ./nrich.nix { };
              })
            ];
          };
        in
        {
          poetry = pkgs.mkShell ({
            # at compile time
            nativeBuildInputs = [
            ];

            # at run time
            buildInputs = with pkgs; [
              # use this package itself
              nrich

              # poetry
              poetry
              python311
              python311Packages.aiohttp
            ];

            shellHook = ''
              # Make sure poetry's venv uses the configured python executable.
              ${pkgs.poetry}/bin/poetry env use --no-interaction ${pkgs.python311}/bin/python3
              ${pkgs.poetry}/bin/poetry install --no-interaction
            '';
          });

          default = pkgs.mkShell ({
            # at compile time
            nativeBuildInputs = [
            ];

            # at run time
            buildInputs = with pkgs; [
              # use this package itself
              nrich
              python311
              python311Packages.aiohttp
            ];

            shellHook = ''
            '';
          });

          nrich = pkgs.mkShell ({
            # at compile time
            nativeBuildInputs = [
            ];

            # at run time
            buildInputs = with pkgs; [
              # use this package itself
              nrich

              python311
              python311Packages.aiohttp
            ];

            shellHook = ''
              python3 -i -c "import nrich"
            '';
          });
        }
      );
    };
}