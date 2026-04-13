# FileWatcher
A utility to make sure folder organization remains as defined in a config file

# Motivation
- Frustration with cluttered Download folder
- Need for something like file juggler on linux
- Need to learn all that it'd take to build a file juggler alt. (it's why i did not fork and improve Organize (which you should look into if you need file organization quick))

# Roadmap
- [x]  MVP : Mechanically move files matching certain criteria to defined folders with no reliance on config
- [ ]  Dry run: Show what script will do before taking action
- [ ]  Scheduling: Run script every X time units so to not mess with half downloaded files among other reasons
- [ ]  Folder watching: Watch certain folders for changes and add those to a pool for changes thatll be effectuated the next automated run
- [ ]  Yaml configuration: Accept yaml configuration for what folders to watch and what structure to enforce in those folders
- [ ]  Action logging: Keep track of all file actions taken
- [ ]  Undo operations: Provide option to undo actions taken by script
