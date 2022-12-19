# fortimanager_model_device_create
This script will create a model device on a FortiManager and set the ZTP reset flag.

When attempting to do zero touch provisioning on FortiManager one method is using the Model Device method.

One issue with Model device is if you create a Model Device and force an upgrade to a paticular code revision 
on the FortiGate the action will blindly upgrade the firmware reguardless of what code it was running on.

This can and often does cause serious issues when trying to push configuraitons from FMG with conflicts. The configuration
on the FortiGate has artifacts from the previous release that FMG doesn't understand.

In 7.0.5 FMG a new feature was added that will allow you to upgrade the code then execute a facotry reset after upgrade 
before provisioning. It requires you to land on 7.0.6 FortiOS and above in your process.

Also in this script it will apply a pre-cli-template on the model device.
