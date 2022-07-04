## Automated Quick Configuration of Vokkero ELITE terminals from a PC via a serial port. 

The python code reads hexadecimal commands in the .dat file, opens a serial port for the terminals and another port for the ELITE Smart Gateway (ESG), i.e. both need to be connected to the computer. 

The selected configuaration is VAR football, with the 4th Referee = master, with an automatic channel selection and the Vokkero noise filter.

A log file is produced in the local directory, specifying the sent messages and the answers.

### Contributing

We use Pull Requests, the integration branch shall be 'develop'

### Versions
QuickConfig\_1stFullVersionOK.py is a fully working version, all in 1 file. 

QuickCOnfig\_newdictionary.py uses json dictionary and classes. 

To do: Merge hex and ascii loops (find way how to convert conveniently, independent of the user).