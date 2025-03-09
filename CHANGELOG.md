# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## [0.1.0](https://github.com/mkdocstrings/griffe-typedoc/releases/tag/0.1.0) - 2025-03-09

<small>[Compare with first commit](https://github.com/mkdocstrings/griffe-typedoc/compare/b45ec86ea0170938f0daec03e4b788cb1c6e9222...0.1.0)</small>

### Build

- Require Python 3.10 minimum (for dataclasses keyword-only arguments) ([8a53b41](https://github.com/mkdocstrings/griffe-typedoc/commit/8a53b41664a9939f83773d55132be4aaac83efd1) by Timothée Mazzucotelli).

### Features

- Support link inline tags and cross-references ([b1cbf2d](https://github.com/mkdocstrings/griffe-typedoc/commit/b1cbf2db36b8e5f9d902d819d91a6ff04156cceb) by Timothée Mazzucotelli). [Issue-mkdocstrings/typescript#5](https://github.com/mkdocstrings/typescript/issues/5)
- Implement prototype loader ([38e203b](https://github.com/mkdocstrings/griffe-typedoc/commit/38e203bee817b5238096df714b7f28e0d6383350) by Timothée Mazzucotelli).
- Generate project with gh:pawamoy/copier-pdm Copier template ([84c4e44](https://github.com/mkdocstrings/griffe-typedoc/commit/84c4e44d7449b13fee183e748b8252771215a152) by Timothée Mazzucotelli).

### Bug Fixes

- Support root module and project when getting source filepath ([0031ad3](https://github.com/mkdocstrings/griffe-typedoc/commit/0031ad3a7e6531f4a30e12f60279d83d168a452e) by Timothée Mazzucotelli). [Issue-mkdocstrings-typescript-25](https://github.com/mkdocstrings/typescript/issues/25)
- Prevent index error when fetching source ([5fdf085](https://github.com/mkdocstrings/griffe-typedoc/commit/5fdf085abaaa4886c6daf6463fb27b2a296c18fe) by Timothée Mazzucotelli). [Issue-24](https://github.com/mkdocstrings/typescript/issues/24)
- Add `mapped` type kind, support `parameter`, `parameter_type` and `template_type` fields in `Type` class ([f9d3818](https://github.com/mkdocstrings/griffe-typedoc/commit/f9d3818199851531dacaf4c915a20ca0b9e6d8b8) by Timothée Mazzucotelli). [Issue-mkdocstrings/typescript#21](https://github.com/mkdocstrings/typescript/issues/21)
- Support `signatures` field in `Interface` class ([3a6e4f4](https://github.com/mkdocstrings/griffe-typedoc/commit/3a6e4f4b6f37bd0d37837450e8c5c9ac75b2859d) by Timothée Mazzucotelli). [Issue-mkdocstrings/typescript#20](https://github.com/mkdocstrings/typescript/issues/20)
- Support `inherited_from` field in `GetSignature`, `SetSignature` and `Accessor` classes ([776eccf](https://github.com/mkdocstrings/griffe-typedoc/commit/776eccf66c232efc8925c5e93f0b29bf107099dd) by Timothée Mazzucotelli). [Issue-mkdocstrings/typescript#19](https://github.com/mkdocstrings/typescript/issues/19)
- Support `index_signatures` field in `TypeLiteral` class ([e4dff88](https://github.com/mkdocstrings/griffe-typedoc/commit/e4dff881e5025bbbfceea58ce6b157613171bbba) by Timothée Mazzucotelli). [Issue-mkdocstrings/typescript#18](https://github.com/mkdocstrings/typescript/issues/18)
- Support `type_parameters` field in various classes ([9d48161](https://github.com/mkdocstrings/griffe-typedoc/commit/9d48161d2298511a5f4c85b5c583b8bdf16ab9cf) by Timothée Mazzucotelli). [Issue-mkdocstrings/typescript#17](https://github.com/mkdocstrings/typescript/issues/17)
- Support various additional fields in various classes ([23d5367](https://github.com/mkdocstrings/griffe-typedoc/commit/23d5367df54144f3f342be7e258288efc07ad278) by Timothée Mazzucotelli). [Issue-mkdocstrings/typescript#16](https://github.com/mkdocstrings/typescript/issues/16)
- Support `implementation_of` field in `SetSignature` class ([f287a22](https://github.com/mkdocstrings/griffe-typedoc/commit/f287a22e989f886909ef5070e611773558a02712) by Timothée Mazzucotelli). [Issue-mkdocstrings/typescript#15](https://github.com/mkdocstrings/typescript/issues/15)
- Support `implementation_of` field in `GetSignature`, `Accessor` and `Property` classes ([7332871](https://github.com/mkdocstrings/griffe-typedoc/commit/7332871048d02aeb5cda619ffe88b5b102e7012e) by Timothée Mazzucotelli). [Issue-mkdocstrings/typescript#14](https://github.com/mkdocstrings/typescript/issues/14)
- Support more fields ([4633158](https://github.com/mkdocstrings/griffe-typedoc/commit/46331581b63bfba48816ad0a6978565cd97fa324) by Timothée Mazzucotelli). [Issue-mkdocstrings/typescript#13](https://github.com/mkdocstrings/typescript/issues/13)
- Add `inherited_from` fields to `Constructor`, `Method`, `CallSignature` and `ConstructorSignature` classes ([ce5ff98](https://github.com/mkdocstrings/griffe-typedoc/commit/ce5ff984d386890f1302bd09a00c37026219addd) by Timothée Mazzucotelli). [Issue-mkdocstrings/typescript#11](https://github.com/mkdocstrings/typescript/issues/11), [Issue-mkdocstrings/typescript#12](https://github.com/mkdocstrings/typescript/issues/12)
- Support `implemented_by`, `implemented_types` and `implementation_of` fields in `Class`, `Interface`, `Method` and `CallSignature` reflections ([9d9fa8f](https://github.com/mkdocstrings/griffe-typedoc/commit/9d9fa8f698f98feb8eb34865d06dc35326cae274) by Timothée Mazzucotelli). [Issue-mkdocstrings/typescript#9](https://github.com/mkdocstrings/typescript/issues/9)
- Support `overwrites` field in `Constructor`, `ConstructorSignature`, `CallSignature` and `Method` reflections, as well as `extended_types` and `extended_by` fields in `Class` reflection ([921512e](https://github.com/mkdocstrings/griffe-typedoc/commit/921512e58029bf12f5142a76b9031a013764ca37) by Timothée Mazzucotelli). [Issue-mkdocstrings/typescript#10](https://github.com/mkdocstrings/typescript/issues/10)
- Add "operator" type kind and same field on types ([2012f6d](https://github.com/mkdocstrings/griffe-typedoc/commit/2012f6d7a5490efc6e6adcb7d49a5a268e83dd58) by Timothée Mazzucotelli). [Issue-mkdocstrings/typescript#6](https://github.com/mkdocstrings/typescript/issues/6)
- Support `parameters` in constructor signatures ([70626a4](https://github.com/mkdocstrings/griffe-typedoc/commit/70626a453e3bf1b7c3868887382bb492648bf519) by Timothée Mazzucotelli). [Issue-mkdocstrings/typescript#8](https://github.com/mkdocstrings/typescript/issues/8)
- Support `prefer_values` and query type ([faa6a9f](https://github.com/mkdocstrings/griffe-typedoc/commit/faa6a9f31cb98080ad199608fff74b0af9cd6e34) by Timothée Mazzucotelli). [Issue-mkdocstrings/typescript#7](https://github.com/mkdocstrings/typescript/issues/7)
- Support `type` on all reflections, support `signatures` on constructors ([78bd842](https://github.com/mkdocstrings/griffe-typedoc/commit/78bd84255664e29d946344aec2dc7584c5e4e4dd) by Timothée Mazzucotelli). [Issue-mkdocstrings/typescript#3](https://github.com/mkdocstrings/typescript/issues/3), [Issue-mkdocstrings/typescript#4](https://github.com/mkdocstrings/typescript/issues/4)
- Support `files` attribute on projects ([89d46be](https://github.com/mkdocstrings/griffe-typedoc/commit/89d46bee949825d3b1316bdff03a5384c438621d) by Timothée Mazzucotelli). [Issue-2](https://github.com/mkdocstrings/typescript/issues/2)
- Be yet more robust when parsing typedoc's output ([23d4619](https://github.com/mkdocstrings/griffe-typedoc/commit/23d4619d49020e558b8b50070c2ea5baf1f253c4) by Timothée Mazzucotelli).
- Don't crash when log level can't be matched in typedoc's output ([032a400](https://github.com/mkdocstrings/griffe-typedoc/commit/032a4006ee56099ad741a1908728ae9c20de6a01) by Timothée Mazzucotelli).
- Support readme field in module classes ([fef7f54](https://github.com/mkdocstrings/griffe-typedoc/commit/fef7f54422c3b70862d916729d2aa876765e71a9) by Timothée Mazzucotelli).

### Code Refactoring

- Expose public objects in top-level module ([34a637c](https://github.com/mkdocstrings/griffe-typedoc/commit/34a637c9495e34f67c470317e2ba2ac3c3501bcb) by Timothée Mazzucotelli).
- Rename dataclasses module to models ([2d00279](https://github.com/mkdocstrings/griffe-typedoc/commit/2d00279507f4d4aaf90f3021208539c2b74896b6) by Timothée Mazzucotelli).
- Move modules into internal folder ([a9c1d44](https://github.com/mkdocstrings/griffe-typedoc/commit/a9c1d44ee329e6180535974dc7bcb39bd10ac308) by Timothée Mazzucotelli).
- Only use dataclasses keyword-only argument on Python 3.10 ([c17530b](https://github.com/mkdocstrings/griffe-typedoc/commit/c17530bdf46eca5b301a518d1a583d09840c05d1) by Timothée Mazzucotelli).
- Improve getting object file path thanks to file registry ([e63a4d5](https://github.com/mkdocstrings/griffe-typedoc/commit/e63a4d5b9b945e28b6680c522af57875241bafac) by Timothée Mazzucotelli).
- Attach parent to more objects ([a103967](https://github.com/mkdocstrings/griffe-typedoc/commit/a103967a3961eeed2749095deb750e37fde90023) by Timothée Mazzucotelli).
