{
  description = "VFRAME: Visual Forensics, Redaction, and Metadata Extraction application";

  # Nixpkgs / NixOS version to use.
  inputs.nixpkgs.url = "nixpkgs/nixos-21.05";

  outputs = { self, nixpkgs }: {

    defaultPackage.x86_64-linux =
      with import nixpkgs { system = "x86_64-linux"; };
      let
        pythonEnv = python38.withPackages (ps: [
          ps.numpy
          ps.toolz
        ]);
      in mkShell {
        packages = [
          pythonEnv

          conda
          opencv
        ];
      };
      # stdenv.mkDerivation {
      #   name = "test";
      #   src = self;
      #   buildPhase = "";
      #   installPhase = "mkdir -p $out/bin; cp -r . $out/";
      #   propagatedDependencies = [
      #     pkgs.opencv
      #     pkgs.conda
      #   ];
      # };

  };
}
