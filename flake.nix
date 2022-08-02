{
  description =
    "VFRAME: Visual Forensics, Redaction, and Metadata Extraction application";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  inputs.poetry2nix.url = "github:nix-community/poetry2nix";

  outputs = { self, nixpkgs, poetry2nix }: rec {
    system = "x86_64-linux";
    overlay = nixpkgs.lib.composeManyExtensions [
      poetry2nix.overlay
      (final: prev: {
        app = prev.poetry2nix.mkPoetryApplication {
          projectDir = ./.;
          python = prev.pkgs.python39;
        };
        env = prev.poetry2nix.mkPoetryEnv {
          projectDir = ./.;
          python = prev.pkgs.python39;
        };
      })
    ];
    pkgsUnfree = import nixpkgs {
      inherit system;
      config.allowUnfree = true; # CUDA
      overlays = [ overlay ];
    };
    pkgs = import nixpkgs {
      inherit system;
      overlays = [ overlay ];
    };
    devShells.${system} = {
      default = pkgs.env.env.overrideAttrs (old: {
        buildInputs = with pkgs; [
          opencv
          python39Packages.poetry
          python39Packages.pytorchWithoutCuda
          python39Packages.torchvision
        ];
      });
      gpu = pkgs.env.env.overrideAttrs (old: {
        buildInputs = with pkgsUnfree; [
          cudatoolkit
          opencv
          python39Packages.poetry
          python39Packages.pytorch-bin
          python39Packages.torchvision-bin
        ];
      });
    };
  };
}
