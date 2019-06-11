"""
DC Motor Controller Script
Applied Mathematics Lab, Massachusetts Institute of Technology
Fischer Moseley January 2019

Interfaces with a Phidget DC Motor Controller over USB
and will update velocity and acceleration using parameters that
the user enters into the terminal.

Also implements a Cyclic mode that will vary the rotational speed
with given parameters.

For any questions, feel free to contact me at fischerm "at" mit.edu

"""
import sys
import time 
from Phidget22.Devices.DCMotor import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *

try:
    from PhidgetHelperFunctions import *
except ImportError:
    sys.stderr.write("\nCould not find PhidgetHelperFunctions. Either add PhdiegtHelperFunctions.py to your project folder "
                      "or remove the import from your project.")
    sys.stderr.write("\nPress ENTER to end program.")
    readin = sys.stdin.readline()
    sys.exit()

#these are operating parameters that Pedro should be able to configure for his run
t_half = 1 #half of how long the device is held at a postive constant speed
t_0 = 1 #how long the deceleration period is 
t_1 = 1 #how long the device is held at a negative constant speed
omega_1 = 100.0
omega_2 = -100.0
n = 5 #how long to repeat for


'''
* Configures the device's DataInterval
* Displays info about the attached Phidget channel.  
* Fired when a Phidget channel with onAttachHandler registered attaches
*
* @param self The Phidget channel that fired the attach event
'''

def onAttachHandler(self):
    
    ph = self

    try:
        #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
        #www.phidgets.com/docs/Using_Multiple_Phidgets for information
        
        print("\nAttach Event:")
        
        """
        * Get device information and display it.
        """
        channelClassName = ph.getChannelClassName()
        serialNumber = ph.getDeviceSerialNumber()
        channel = ph.getChannel()
        if(ph.getDeviceClass() == DeviceClass.PHIDCLASS_VINT):
            hubPort = ph.getHubPort()
            print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")
        else:
            print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                    "\n\t-> Channel:  " + str(channel) + "\n")
    
        """
        * Set the DataInterval inside of the attach handler to initialize the device with this value.
        * DataInterval defines the minimum time between VelocityUpdate events.
        * DataInterval can be set to any value from MinDataInterval to MaxDataInterval.
        """
        print("\tSetting DataInterval to 10ms")
        try:
            ph.setDataInterval(100)
        except PhidgetException as e:
            sys.stderr.write("Runtime Error -> Setting DataInterval: \n\t")
            DisplayError(e)
            return
        
    except PhidgetException as e:
        print("\nError in Attach Event:")
        DisplayError(e)
        traceback.print_exc()
        return

"""
* Displays info about the detached Phidget channel.
* Fired when a Phidget channel with onDetachHandler registered detaches
*
* @param self The Phidget channel that fired the attach event
"""
def onDetachHandler(self):

    ph = self

    try:
        #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
        #www.phidgets.com/docs/Using_Multiple_Phidgets for information
        
        print("\nDetach Event:")
        
        """
        * Get device information and display it.
        """
        channelClassName = ph.getChannelClassName()
        serialNumber = ph.getDeviceSerialNumber()
        channel = ph.getChannel()
        if(ph.getDeviceClass() == DeviceClass.PHIDCLASS_VINT):
            hubPort = ph.getHubPort()
            print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")
        else:
            print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                    "\n\t-> Channel:  " + str(channel) + "\n")
        
    except PhidgetException as e:
        print("\nError in Detach Event:")
        DisplayError(e)
        traceback.print_exc()
        return

"""
* Writes Phidget error info to stderr.
* Fired when a Phidget channel with onErrorHandler registered encounters an error in the library
*
* @param self The Phidget channel that fired the attach event
* @param errorCode the code associated with the error of enum type ph.ErrorEventCode
* @param errorString string containing the description of the error fired
"""
def onErrorHandler(self, errorCode, errorString):

    sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")

"""
* Outputs the DCMotor's most recently reported velocity.
* Fired when a DCMotor channel with onVelocityUpdateHandler registered meets DataInterval criteria
*
* @param self The DCMotor channel that fired the VelocityUpdate event
* @param velocity The reported velocity from the DCMotor channel
"""
def onVelocityUpdateHandler(self, velocity):

    #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
    #www.phidgets.com/docs/Using_Multiple_Phidgets for information

    # I'm commenting out this line because it's a little verbose
    # print("[Velocity Event] -> Velocity: " + str(velocity))
    pass
    
"""
* Prints descriptions of how events related to this class work
"""   

"""
* Creates, configures, and opens a DCMotor channel.
* Provides interface for controlling TargetVelocity of the DCMotor.
* Closes out DCMotor channel
*
* @return 0 if the program exits successfully, 1 if it exits with errors.
"""
def main():
    try:
        """
        * Allocate a new Phidget Channel object
        """
        try:
            ch = DCMotor()
        except PhidgetException as e:
            sys.stderr.write("Runtime Error -> Creating DCMotor: \n\t")
            DisplayError(e)
            raise
        except RuntimeError as e:
            sys.stderr.write("Runtime Error -> Creating DCMotor: \n\t" + e)
            raise

        """
        * Set matching parameters to specify which channel to open
        """
        #You may remove this line and hard-code the addressing parameters to fit your application
        #channelInfo = AskForDeviceParameters(ch)
        
        ch.setDeviceSerialNumber(473647)
        ch.setHubPort(-1)
        ch.setIsHubPortDevice(False)
        ch.setChannel(0)   
        
        """
        * Add event handlers before calling open so that no events are missed.
        """
        print("\n--------------------------------------")
        print("\nSetting OnAttachHandler...")
        ch.setOnAttachHandler(onAttachHandler)
        
        print("Setting OnDetachHandler...")
        ch.setOnDetachHandler(onDetachHandler)
        
        print("Setting OnErrorHandler...")
        ch.setOnErrorHandler(onErrorHandler)
        
        print("\nSetting OnVelocityUpdateHandler...")
        ch.setOnVelocityUpdateHandler(onVelocityUpdateHandler)
        
        """
        * Open the channel with a timeout
        """
        print("\nOpening and Waiting for Attachment...")
        
        try:
            ch.openWaitForAttachment(5000)
        except PhidgetException as e:
            PrintOpenErrorMessage(e, ch)
            raise EndProgramSignal("Program Terminated: Open Failed")

        print("--------------------\n"
        "\nInput a desired velocity/acceleration value and press ENTER\n"
        'Velocity Syntax: "v100" will set the motor speed to 100% in the positive direction \n'
        'and calling "v-52" will set the motor speed to 52% in the negative direction \n'
        '\nAcceleration Syntax: "a25" will set the motor acceleration to 25dty/s^2'
        "\nThe motor cannot accelerate any faster than 62.5 dty/s^2 or slower than 0.28 dty/s^2\n"
        '\nTo enter cyclic mode, press "c" or "C" and the program will run with stored parameters'
        '\nTo modify the cyclic mode parameters, edit this python file and edit the variables at'
        '\nthe top of the file.\n'

        '\nNote: Due to some limitations within Python, once cyclic mode is engaged the only'
        '\nway to quit cyclic mode is to use Control + C (Command + C on a Mac). This ends the'
        '\nentire program, and will stop the motor instantly. For this reason, if please consider'
        '\nusing a small number of cycles so that you do not have to wait for them all to finish\n'


        '\nInput "Q" and press ENTER to come to a hard stop\n'
        '\nInput "S" and press ENTER to come to a soft stop\n')

        end = False

        while (end != True):
            buf = sys.stdin.readline(100)
            if not buf:
                continue

            if (buf[0] == 'Q' or buf[0] ==  'q'):
                end = True
                continue
            
            if (buf[0] == 'v' or buf[0] == 'V'): #set velocity of the motor
                try:
                    velocity = float(buf[1:])
                except ValueError as e:
                    print("Input must be a number, or Q to quit.")
                    continue

                if (velocity > 100.0):
                    velocity = 100.0
                    print("WARNING: MAXIMUM velocity is +/- 100%")

                if (velocity < -100.0):
                    velocity = -100.0
                    print("WARNING: MAXIMUM velocity is +/- 100%")

                print("Setting DCMotor TargetVelocity to " + str(velocity) + "%")
                ch.setTargetVelocity(velocity/100)
            
            elif(buf[0] == 'a' or buf[0] == 'A'): #set acceleration of the motor
                try:
                    acceleration = float(buf[1:])
                except ValueError as e:
                    print("Input must be a number, V for velocity, A for acceleration or Q to quit.")
                    continue
                        
                if (acceleration > 62.5):
                    acceleration = 62.5
                    print("WARNING: Maximum acceleration is 62.5 dty/s^2")     

                if (acceleration < 0.28):
                    acceleration = 0.28
                    print("WARNING: Minimum acceleration is 0.28 dty/s^2")  

                print("Setting DCMotor Acceleration to " + str(acceleration) + " dty/s^2")
                ch.setAcceleration(acceleration)

            elif(buf[0] == 'c' or buf[0] == 'C'):
                print("Entering Cycle Mode")
                for i in range(n):
                    print("Beginning cycle " + str(i+1))
                    print("Setting Velocity to " + str(omega_1) + "%")
                    ch.setTargetVelocity(omega_1/100)
                    time.sleep(t_half)
                    #calculate acceleration
                    ch.setAcceleration(abs(((omega_1/100)-(omega_2/100))/t_0))
                    print("Setting Velocity to " + str(omega_2) + "%")
                    ch.setTargetVelocity(omega_2/100)
                    time.sleep(t_0)
                    time.sleep(t_1)
                    print("Setting Velocity to " + str(omega_1) + "%")
                    ch.setTargetVelocity(omega_1/100)
                    time.sleep(t_0)
                    time.sleep(t_half)
                print("Exiting Cycle Mode")
                print("Velocity currently set to " + str(ch.getVelocity()*100) + "%")

            elif(buf[0] == 's' or buf[0] == 'S'):
                print("Initiating Soft Stop")
                ch.setAcceleration(ch.getMinAcceleration())
                ch.setTargetVelocity(0)
                while(ch.getVelocity()>0):
                    time.sleep(0.1)
                print("Motor Stopped")
                end = True
                continue

            else:
                print("WARNING: Invalid Command")

        '''
        * Perform clean up and exit
        '''
        

        #clear the VelocityUpdate event handler 
        ch.setOnVelocityUpdateHandler(None)  

        print("Cleaning up...")
        ch.close()
        print("\nExiting...")
        return 0

    except PhidgetException as e:
        sys.stderr.write("\nExiting with error(s)...")
        DisplayError(e)
        traceback.print_exc()
        print("Cleaning up...")
        #clear the VelocityUpdate event handler 
        ch.setOnVelocityUpdateHandler(None)  
        ch.close()
        return 1
    except EndProgramSignal as e:
        print(e)
        print("Cleaning up...")
        #clear the VelocityUpdate event handler 
        ch.setOnVelocityUpdateHandler(None)  
        ch.close()
        return 1
    finally:
        pass

main()

