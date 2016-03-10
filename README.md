# Generate



Generator for Android ContentProvider 
=================================

based on https://github.com/BoD/android-contentprovider-generator/ but 
rewritten in Python jinja2 template system


This tool generates an Android ContentProvider, representation layer and 
listener for changes in the applicaitons database.

It takes a set of models (a.k.a "table") definitions as the input, and 
generates:
- a `ContentProvider` class
- a `SQLiteOpenHelper` class
- a `SQLiteOpenHelperCallbacks` class
- one `Columns` class per model
- one `Cursor` class per model
- one `ContentValues` class per model
- one `Selection` class per model
- one `Model` interface per model
- one listener per model
- one presenter layers per model
- one representation class per model


How to use
----------

### The `_config.json` file

This is where you declare a few parameters that will be used to generate the code.

These are self-explanatory so here is an example:
```json
{
	"projectPackageId": "com.example.app",
	"authority": "com.example.app.provider",
	"providerJavaPackage": "com.example.app.provider",
	"providerClassName": "ExampleProvider",
	"sqliteOpenHelperClassName": "ExampleSQLiteOpenHelper",
	"sqliteOpenHelperCallbacksClassName": "ExampleSQLiteOpenHelperCallbacks",
	"databaseFileName": "example.db",
}
```

### Model files

Create one file per model, naming it `<model_name>.json`.
Inside each file, declare your fields (a.k.a "columns") with a name and a type.
You can also optionally declare a default value, an index flag, a documentation and a nullable flag.

Currently the type can be:
- `String` (SQLite type: `TEXT`)
- `Integer` (`INTEGER`)
- `Long` (`INTEGER`)
- `Float` (`REAL`)
- `Double` (`REAL`)
- `Boolean` (`INTEGER`)
- `Date` (`INTEGER`)
- `byte[]` (`BLOB`)
- `enum` (`INTEGER`).

You can also optionally declare table constraints.

Here is a `person.json` file as an example:

```json
{
    "documentation": "LedStatus model.",
    "fields": [
        {
            "name": "led_status",
            "type": "String"
        },
        {
            "name": "iot_device",
            "type": "String"
        },        
		{
            "name": "origin",
            "type": "String"
        },        
		{
            "name": "time_stamp_x_gateway",
            "type": "String"
        },        
		{
            "name": "ack_m",
            "type": "Boolean"
        },        
		{
            "name": "ack_g",
            "type": "Boolean"
        }, 		{
            "name": "ack_c",
            "type": "Boolean"
        }
    ]
}
```

Notes:
- An `_id` primary key field is automatically (implicitly) declared for all entities. It must not be declared in the json file.
- `nullable` is optional (true by default).
- if `documentation` is present the value will be copied in Javadoc blocks in the generated code.

By convention, you should name your models and fields in lower case with words 
separated by '_', like in the example above.

### The `header.txt` file (optional)

If a `header.txt` file is present, its contents will be inserted at the top of every generated file.


### Run the tool

`python generate.py -i <input folder> -o <output folder>`
- Input folder: where to find `_config.json` and your model json files
- Output folder: where the resulting files will be generated

### Use the generated files



Similar tools
-------------
Based on the idea in 
- https://github.com/BoD/android-contentprovider-generator

this project adds presenter layers, listner, and representation layers for 
the data model.

Licence
-------

          _______  _______  _______  _______  _
 |\     /|(  ___  )(  ____ )(       )(  ___  )( (    /||\     /|
 | )   ( || (   ) || (    )|| () () || (   ) ||  \  ( |( \   / )
 | (___) || (___) || (____)|| || || || |   | ||   \ | | \ (_) /
 |  ___  ||  ___  ||     __)| |(_)| || |   | || (\ \) |  \   /
 | (   ) || (   ) || (\ (   | |   | || |   | || | \   |   ) (
 | )   ( || )   ( || ) \ \__| )   ( || (___) || )  \  |   | |
 |/     \||/     \||/   \__/|/     \|(_______)|/    )_)   \_/

 Copyright (C) 2016 Laurynas Riliskis

 Licensed under the Apache License, Version 2.0 (the "License")
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.

__*Just to be absolutely clear, this license applies to this program itself,
not to the source it will generate!*__
