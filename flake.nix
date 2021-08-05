{
  description = "VFRAME: Visual Forensics, Redaction, and Metadata Extraction application";

  # Nixpkgs / NixOS version to use.
  inputs.nixpkgs.url = "nixpkgs/nixos-21.05";

  outputs = { self, nixpkgs }: {

    packages.x86_64-linux.vframe =
      let
        buildVframeApp = { lib, pkgs, buildPythonApplication }:

          buildPythonApplication rec {
            pname = "vframe";
            version = "0";

            src = ./.;

            proparagedBuildInputs = [
              pkgs.opencv
            ];

            meta = with lib; {
              homepage = "https://github.com/ngi-nix/vframe";
              description = "VFRAME: Visual Forensics, Redaction, and Metadata Extraction application";
              licence = licenses.mit;
            };
          };
        pkgs = import nixpkgs { system = "x86_64-linux"; };
      in
      pkgs.callPackage buildVframeApp {
        buildPythonApplication = pkgs.python38Packages.buildPythonPackage;
      };


    defaultPackage.x86_64-linux = self.packages.x86_64-linux.vframe;

  };
}
