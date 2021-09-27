# Houdini Package Template
Template repo for creating simple (or not so simple) Houdini Packages.

- [Houdini Package Template](#houdini-package-template)
  - [Overview](#overview)
  - [Getting Started](#getting-started)
  - [Installing Your Package](#installing-your-package)
    - [Method 1: Packages live in the `packages` directory](#method-1-packages-live-in-the-packages-directory)
      - [Setup](#setup)
    - [Method 2: Packages live somewhere else](#method-2-packages-live-somewhere-else)
    - [Caveats](#caveats)
  - [Tools for Different Houdini Versions](#tools-for-different-houdini-versions)
    - [Alternative: Per-build package](#alternative-per-build-package)
    - [Another Alternative: Who cares about the build version?](#another-alternative-who-cares-about-the-build-version)
  - [Template Contents](#template-contents)
    - [Package `.json`](#package-json)
    - [houdiniX.Y](#houdinixy)
    - [pythonX.7libs](#pythonx7libs)
      - [Packages](#packages)
      - [Modules](#modules)
    - [MainMenuCommon.xml](#mainmenucommonxml)
    - [toolbar](#toolbar)
    - [help/nodes](#helpnodes)
    - [`initialize.py`](#initializepy)


## Overview

This repo is meant to be a quick jumping off point for creating a Houdini
package. You likely won't need everything in here, but several common files and
folders have been included as a good start.

## Getting Started

1. Create a repository from this template

    [![Creating a repo from a template](https://jamesrobinsonvfx.com/assets/projects/houdini-package-template/images/repo-from-template.gif)](https://jamesrobinsonvfx.com/assets/projects/houdini-package-template/images/repo-from-template.gif)

2. Clone your new repository to your local machine
    ```
    git clone git@github.com:jamesrobinsonvfx/demo_tool.git
    ```

3. Open the repository and run `./initialize.py` ([See below for extra use instructions](#initializepy))

4. Start building your tool!

5. Zip it up and share it with others *(Optional)*

    Run the following to create a `.zip` archive without any of the extra git
    fluff (See the included `.gitattributes` file for a list of excluded files)

    ```bash
    git archive --format zip --output ../demo_tool.zip main
    ```

    If you'd like to do an actual [release](http://github.com/jamesrobinsonvfx/houdini_package_template/releases/latest), read
    about how to do that on the [GitHub docs](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository). You'll be able to add your  `.zip` archive as part of the release links.

    You can tell people to grab it by pointing them to
    ```
    https://github.com/jamesrobinsonvfx/demo_tool/releases/latest/download/demo_tool.zip
    ```

## Installing Your Package
At some point, you'll want to install your package into a Houdini session for everyday use and testing.


In order for Houdini to be able to include your tools in a session, it needs to
be able to find them. Houdini looks in a set of [paths and
locations](https://www.sidefx.com/docs/houdini/basics/config.html#path) and
loads in stuff that it finds along the way. Commonly, these would be things like
Python libraries, HDAs, custom shelves, etc. You *could* just manually copy the
contents of each of these to their respective folders (`python2.7libs`, `hda`,
`toolbar`...), but keeping track of all that can become a nightmare! With
Houdini Packages, you can keep all that stuff together in one location, and with
a specially formatted *package* `.json` file, you can tell Houdini where to look
for it.

There's a multitude of ways you can configure your packages to load. I highly recommend visiting the
[Houdini Packages documentation](https://www.sidefx.com/docs/houdini/ref/plugins.html) for more detailed info.

Outlined below are two favorite ways of setting up and loading packages. Package
`.json` files can be placed in any `packages` folder within a [Houdini Location](https://www.sidefx.com/docs/houdini/basics/config.html#path).
For studio-wide tools, that's usually best located at your facility's `$HSITE`.
For single users you'll probably want to use your `$HOUDINI_USER_PREF_DIR` if
you don't have `$HSITE` set up. I will be using `$HOUDINI_USER_PREF_DIR` to make
it easy to follow along.

### Method 1: Packages live in the `packages` directory

With this method, package folders and their `.json` package files live directly inside
`$HOUDINI_USER_PREF_DIR/packages`.

> Houdini will *not* automatically search for `.json` files inside of subfolders
> within the `packages` directory.

#### Setup

Assuming your package is called `demo_tool`.

1. Copy your Houdini Package folder to `$HOUDINI_USER_PREF_DIR/packages/demo_tool`
2. Copy `demo_tool.json` from
   `$HOUDINI_USER_PREF_DIR/packages/demo_tool` to `$HOUDINI_USER_PREF_DIR/packages`

Your `$HOUDINI_USER_PREF_DIR` directory structure should now resemble:
```
houdini18.5
└── packages/
    ├── some_other_package/
    │   ├── houdini18.5/
    │   └── some_other_package.json
    ├── demo_tool/
    │   ├── houdini18.5/
    │   └── demo_tool.json
    ├── some_other_package.json
    └── demo_tool.json
```

`demo_tool.json` can be quite simple:
```json
{
    "path": "$HOUDINI_PACKAGE_PATH/demo_tool/houdini18.5"
}
```

`path` is a shorthand keyword we can use to insert a location to the `$HOUDINI_PATH`.

When used in a package `.json` file, the
`$HOUDINI_PACKAGE_PATH` variable refers to the location of the package that is
currently being read.

There are certain conditional statements (if/then) we can add to load different
folders based on the Houdini version. See the actual
`houdini_package_template.json` file for a more detailed package definition that
does that.


### Method 2: Packages live somewhere else

It's not uncommon to have a separate location on disk that holds 3rd party tools. In
this case, we can *dynamically* add locations to tell Houdini to search in using
the `package_path` keyword.

This this scenario, we have a `packages` folder located inside a known Houdini
location, like `$HOUDINI_USER_PREF_DIR`. There is just one `.json` file inside.
Its job is to point to other places where packages might live:

```
houdini18.5
└── packages/
    └── packages.json
```

```json
{
    "env": [
        {
            "STUDIO_TOOLS": "/prod_server/studio_tools"
        }
    ],

    "package_path": [
        "$STUDIO_TOOLS/cool_solver",
        "$STUDIO_TOOLS/demo_tool",
        "$STUDIO_TOOLS/qlib",
    ]
}
```

Elsewhere on disk, we have a folder called `studio_tools`, filled with 3rd party
Houdini Packages.

```
prod_server
└── studio_tools/
    ├── cool_solver/
    ├── demo_tool/
    ├── qlib/
    ├── render_engine/
    └── some_other_package/
```

Each Houdini Package keeps its `[package_name].json` file inside. No need to
move/copy it like [Method 1](#method-1-packages-live-in-the-packages-directory).

```json
{
    "path": "$HOUDINI_PACKAGE_PATH/houdini18.5"
}
```

This method can be a great way to keep a bunch of 3rd party tools organized.
It also makes it easy to programatically add/remove packages, or even have
multiple locations, such as a set of "production" packages and another set of
"experimental" or "dev" pacakges.


As you can see, both ways have their pros and cons. And these certainly *are not* the only possible configurations!

### Caveats
If you notice that HDAs/OTLs aren't loading, but everything else in your package
is, you might need to explicitly set `$HOUDINI_OTLSCAN_PATH`. While this
*shouldn't* be necesary, I've found that some tools/wrappers can block OTLs being
loaded from custom additions to `$HOUDINI_PATH`. Setting this environment
variable in your package is pretty straightforward:

```json
{
    "path": "$DEMO_TOOL_INSTALL_DIR",
    "env": [
        {
            "DEMO_TOOL_INSTALL_DIR": [
                {
                    "houdini_version >= '18.0' and houdini_version < '18.5'": "$HOUDINI_PACKAGE_PATH/demo_tool/houdini18.0"
                },
                {
                    "houdini_version >= '18.5' and houdini_version < '19.0'": "$HOUDINI_PACKAGE_PATH/demo_tool/houdini18.5"
                }
            ]
        },
        {
            "HOUDINI_OTLSCAN_PATH": {
                "value": "$DEMO_TOOL_INSTALL_DIR/hda",
                "method": "append"
            }
        }
    ]
}
```

> This used to be included in the template, but this should be more of an edge
> case, so it has been removed.

## Tools for Different Houdini Versions
Every year, SideFX releases a new minor version of Houdini (18.**0**, 18.**5**,
etc.). Sometimes they make pretty sweeping changes that can cause your tools not
to work between versions.

Rather than fighting this and trying to make your tool work for every release of
Houdini, you can just create a new version of your tool to work with the next release.

The easiest way to release your stuff for a new version is to simply copy your
latest `houdiniX.Y` folder, update the number, and see if it works! For
example, when Houdini 19.0 is released, you can do the following:

1. Copy `houdini18.5` and all of its contents
2. Paste it
3. Rename `houdini18.5` to `houdini19.0`
4. Update the `demo_tool.json` file to load from that location
   when using `houdini19.0`

   ```json
   {"houdini_version >= '19.0' and houdini_version < '19.5'": "$HOUDINI_PACKAGE_PATH/demo_tool/houdini19.0"}
   ```

### Alternative: Per-build package

In some cases, especially for tools that might depend on specific production
builds (render engines, custom HDK nodes), it might be important to have a
unique release of your tool per *build*.

In this case, instead of having a `houdini18.5` folder, you might have multiple
folders named for each build number, ie. `18.5.496`, `18.5.593`
```
demo_tool
├── 18.5.496/
└── 18.5.596/
    ├── dso/
    └── hda/
...
```

Instead of writing conditional statements for *every single build*, there's actually an
undocumented shorthand we can use:

```json
{
    "path": "$HOUDINI_PACKAGE_PATH/${HOUDINI_VERSION}"
}
```
### Another Alternative: Who cares about the build version?

It's not actually necessary to have separate versions of your tool for different
Houdini versions. As long as you have properly named folders that follow the
structure of `$HFS/houdini`.

```
demo_tool
├── hda/
│   └── studio_cooltool.hda
└── python3.7libs/
    └── package_utils.py
```

```json
{
    "path": "$HOUDINI_PACKAGE_PATH/demo_tool"
}
```

This also works, but remember it could be a little trickier to maintain across
Houdini versions.

## Template Contents

This Houdini Package structure mimics the one you'd find in `$HH` (aka
`$HFS/houdini`). This makes it easy for Houdini to pick up its contents. When
you tell Houdini to add a directory to the `$HOUDINI_PATH`, any folders that
match the name/structure found in `$HH` will be made available to you in your houdini
session.

> `$HFS` is the location of the Houdini installation. You can type this in a
> File Browser from within Houdini to see exactly where this is.

If you ever want to add more folders inside, check out the contents of `$HH`.
For example, if you wanted to add some testing geometry to your package, refer
to `$HH` for where that might be (probably`geo`). Or maybe you
want to extend the Gear Menu in the parameter editor with some of your own custom functionality. In `$HH` you
see that there is a `ParmGearMenu.xml` file. To mimic the structure, you would
simply add your own `ParmGearMenu.xml` file right inside the
`houdini18.5` directory. I think you get the point!

Several common directories and files have been included. Any of the files/folders inside `houdiniX.Y` can be removed if they aren't
needed for your project. At a bare minimum, like a package with a single HDA, your package structure should
probably look something like this:
```
demo_tool
├── houdini18.5/
│   └── hda/
│       └── jamesr_cooltool.hda
└── demo_tool.json
```

### Package `.json`
This is the file that tells Houdini how to load your tool.

Houdini will search folders called `packages` for `.json` files. These `.json`
files can be used to set environment variables when Houdini launches, and add
things to the `$HOUDINI_PATH` so that they are made available to you in the
Houdini session.

Think of it like `houdini.env`, but easier to deal with.

### houdiniX.Y
Directory that mirrors `$HFS/houdini`. By naming it after each minor release, we
can easily maintain our tools for forward and backward compatibility.

### pythonX.7libs

With Python 3 being the current VFX standard, and more and more DCCs supporting
it, `python3.7libs` has been added to this template as a starting point. A few
things to note:

- You can have both `python2.7libs` and `python3.7libs` in the same project.
  Depending on your Houdini installation, if you're launching with a Python 3
  build, Houdini will use the packages/modules found in `python3.7libs`.
- Python 3 does not necessary require an `__init__.py` file like Python 2.7 does.

#### Packages
- You might want a whole Python package that you can import, so one named after
  the Houdini package has been included.

#### Modules
- If your Houdini package only needs a single python module (`.py` file), you can delete
  the folder inside `pythonX.7libs`, and simply put your python file directly in
  there.

### MainMenuCommon.xml
Not every tool needs a dropdown menu (nor should they all get one!), but
included is a simple template example for where it would need to go, as well as some
boilerplate XML that creates a menu named after your package.

### toolbar
`houdiniX.Y/toolbar` is where any `.shelf` files live. Some packages really benefit from
having artist-friendly shelf tools to help make using your tools a bit easier. Inside
is some more boilerplate XML to setup a simple shelf named after your package.

> Remember if you add any tools to you custom shelf in Houdini, make sure to set
> the save location to your shelf! Unfortunately, Houdini does *not* remember
> your save choices, and will default to saving to the default shelf in your preferences directory!
>
>[![Saving a shelf tool](https://jamesrobinsonvfx.com/assets/projects/houdini-package-template/images/save-shelf-tool.png)](https://jamesrobinsonvfx.com/assets/projects/houdini-package-template/images/save-shelf-tool.png)

### help/nodes
Help cards for any of your tools/assets can live either directly on the assets
themselves, or someplace on disk. Included is the structure for where you need
to store custom help card docs, as well as a basic starting template.

> Take note of the naming scheme- if you're following [SideFX's recommended
> naming and versioning
> scheme](https://www.sidefx.com/docs/houdini/assets/projects//namespaces.html), you'll
> probably have tools named like this:
> ```
> jamesr::inspectnodedata::1.00
> ```
> where `jamesr` is the *namespace*. The help file for such a node would be called
> ```
> jamesr--inspectnodedata.txt
> ```

### `initialize.py`

This script runs a short command-line wizard that lets you set the package name
and title. It should be run before making any additions/changes to the template.

**macOS / Linux**
```
./initialize.py
```

**Windows**
```
python initialize.py
```

If you prefer to do it in one line, you can add the package name and title as
command-line arguments:

```
./initialize.py [title] [package_name]
```
ie.
```
./initialize.py "Demo Tool" demo_tool
```

[![Initialize](https://jamesrobinsonvfx.com/assets/projects/houdini-package-template/images//initialize.gif)](https://jamesrobinsonvfx.com/assets/projects/houdini-package-template/images//initialize.gif)

You could totally just manually hunt for everything called `houdini_package_template`, and the tags `{% package_name %}`, `{% Package Title
%}` and `{% PACKAGE_NAME_UPPER %}`, and replace them manually. Or you can
use the script (just use the script).