{
python311Packages,
lib,
}: python311Packages.buildPythonPackage rec {
  pname = "nrich";
  version = "0.1.0";
  src = ./.;
  format = "pyproject";

  # has no tests
  doCheck = false;

  propagatedBuildInputs = [
    python311Packages.aiohttp
    python311Packages.poetry-core
  ];

  meta = {
    description = "Python equivalent of the rust [nrich](https://gitlab.com/shodan-public/nrich) program, developed by Shodan";
    license = lib.licenses.gpl3;
    changelog = "https://github.com/pimvh/nrich/releases/v${version}/";
    maintainers = with lib.maintainers; [ pimvh ];
  };
}
