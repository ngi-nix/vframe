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
        vframe-app = prev.poetry2nix.mkPoetryApplication {
          projectDir = ./.;
          python = prev.pkgs.python39;
        };
        vframe-env = prev.poetry2nix.mkPoetryEnv {
          projectDir = ./.;
          python = prev.pkgs.python39;
        };
      })
    ];
    pkgs = import nixpkgs {
      inherit system;
      overlays = [ overlay ];
    };
    devShells.${system}.default = pkgs.vframe-env.env.overrideAttrs (old: {
      buildInputs = with pkgs; [ python39Packages.poetry opencv ];
    });
  };
}
