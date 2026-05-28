# dataModel.d.ts

This code is generated

These exports are not directly available in the `convex` package!

Instead you must run `npx convex dev` to create `convex/_generated/dataModel.d.ts`.

Generated data model types.

## Types[​](#types "Direct link to Types")

### TableNames[​](#tablenames "Direct link to TableNames")

Ƭ **TableNames**: `string`

The names of all of your Convex tables.

***

### Doc[​](#doc "Direct link to Doc")

Ƭ **Doc**`<TableName>`: `Object`

The type of a document stored in Convex.

#### Type parameters[​](#type-parameters "Direct link to Type parameters")

| Name        | Type                                | Description                                             |
| ----------- | ----------------------------------- | ------------------------------------------------------- |
| `TableName` | extends [`TableNames`](#tablenames) | A string literal type of the table name (like "users"). |

***

### Id[​](#id "Direct link to Id")

An identifier for a document in Convex.

Convex documents are uniquely identified by their `Id`, which is accessible on the `_id` field. To learn more, see [Document IDs](/database/document-ids.md).

Documents can be loaded using `db.get(tableName, id)` in query and mutation functions.

IDs are just strings at runtime, but this type can be used to distinguish them from other strings when type checking.

This is an alias of [`GenericId`](/api/modules/values.md#genericid) that is typed for your data model.

#### Type parameters[​](#type-parameters-1 "Direct link to Type parameters")

| Name        | Type                                | Description                                             |
| ----------- | ----------------------------------- | ------------------------------------------------------- |
| `TableName` | extends [`TableNames`](#tablenames) | A string literal type of the table name (like "users"). |

***

### DataModel[​](#datamodel "Direct link to DataModel")

Ƭ **DataModel**: `Object`

A type describing your Convex data model.

This type includes information about what tables you have, the type of documents stored in those tables, and the indexes defined on them.

This type is used to parameterize methods like [`queryGeneric`](/api/modules/server.md#querygeneric) and [`mutationGeneric`](/api/modules/server.md#mutationgeneric) to make them type-safe.
