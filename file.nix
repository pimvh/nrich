{
  buildPythonApplication,
  python311Packages
, lib
,
}:
buildPythonApplication rec {
  pname = "nrich";
  version = "0.1.0";
  src = ./.;
  format = "pyproject";

  # has no tests
  doCheck = false;

  propagatedBuildInputs = [
    python311Packages.aiohttp
  ];

  meta = {
    description =
      "Python equivalent of the rust [nrich](https://gitlab.com/shodan-public/nrich) program, developed by Shodan";
    #license = lib.license.gpl20;
    changelog = "https://github.com/pimvh/nrich/releases/v${version}/";
    maintainers = with lib.maintainers; [ pimvh ];
  };
}
