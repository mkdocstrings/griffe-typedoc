- Generated docs for squidfunk's monorepo using typedoc (github issue on typedoc, conversation with martin)
- Looked at typedoc's source code to get the "kind" mapping
- Created all necessary enums
- Created a dataclass for each kind
- Listed all attr for each kind, sorting unique, to guess common/mandatory/optional args
- Grep JSON to see possible values
- Continuously try to load JSON data, fill in missing dataclass fields, looking at values in VSCode's debugger
- Look at loaded data, search for dicts still not represented by dataclasses


function: id, name, variant, kind, flags, sources, signatures
interface: id, name, variant, kind, flags, comment, children, groups, sources
interface: id, name, variant, kind, flags, comment, children, groups, sources, extendedTypes
interface: id, name, variant, kind, flags, comment, children, groups, sources, typeParameters, extendedBy
method: id, name, variant, kind, flags, sources, signatures
module: id, name, variant, kind, flags, children, groups, packageVersion
module: id, name, variant, kind, flags, children, groups, sources
module: id, name, variant, kind, flags, sources
namespace: id, name, variant, kind, flags, children, groups, sources
project: id, name, variant, kind, flags, children, packageName, readme
property: id, name, variant, kind, flags, sources, type
property: id, name, variant, kind, flags, sources, type, inheritedFrom
property: id, name, variant, kind, flags, sources, type, overwrites
reference: id, name, variant, kind, flags, sources, target
type_alias: id, name, variant, kind, flags, comment, sources, type
variable: id, name, variant, kind, flags, comment, sources, type, defaultValue
variable: id, name, variant, kind, flags, sources, type