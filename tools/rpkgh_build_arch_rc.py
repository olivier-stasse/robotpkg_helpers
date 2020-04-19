#!/usr/bin/python3
import os
import sys
import notify2 
from robotpkg_helpers import RobotpkgTests
from robotpkg_helpers import HandlingImgs,RobotpkgArchitectureReleaseCandidate

class RpkghBuildArchReleaseCandidate:

    def __init__(self):

        self.RED =  '\033[0;31m'
        self.GREEN= '\033[0;32m'
        self.PURPLE='\033[0;35m'
        self.NC =   '\033[0m'

        # Load the arch distribution file.
        self.arch_release_candidate = RobotpkgArchitectureReleaseCandidate()
        self.arch_release_candidate.handle_options()
        self.build_release_candidate()
        
        
    def notify_ok(self, notif_title, notif_message):
        notify2.init('Robotpkg Helpers Notify')
        n = notify2.Notification(notif_title,  
                                 notif_message,  
                                 icon="/usr/share/icons/oxygen/64x64/actions/dialog-ok-apply.png"
                                 ) 
        n.set_urgency(notify2.URGENCY_NORMAL) 
        n.show() 
        n.set_timeout(15000)

    def notify_wrong(self, notif_title, notif_message):
        notify2.init('Robotpkg Helpers Notify')
        n = notify2.Notification(notif_title,  
                                 notif_message,  
                                 icon="/usr/share/icons/oxygen/64x64/status/dialog-error.png"
                                 ) 
        n.set_urgency(notify2.URGENCY_NORMAL) 
        n.show() 
        n.set_timeout(15000)
        
    def build_release_candidate(self):
        aHandlingImg = HandlingImgs(self.arch_release_candidate)

        # Perform the deployment in arpgtestrc
        arpgtestrc = \
            RobotpkgTests(anArchReleaseCandidate=self.arch_release_candidate,
                          debug=int(aHandlingImg.robotpkg_mng_vars['verbosity']))
        if arpgtestrc.perform_test_rc():
            # If it worked then compile the package specified in targetpkg
            if 'targetpkg' in self.arch_release_candidate.robotpkg_mng_vars:
                # Test if this is a list or not
                if isinstance(anArchReleaseCandidate.robotpkg_mng_vars['targetpkg'],str) :
                    arpgtestrc.compile_package(anArchReleaseCandidate.robotpkg_mng_vars['targetpkg'])
                    self.notify_ok("Robotpkg helpers",
                                   "Compiling "+anArchReleaseCandidate.robotpkg_mng_vars['targetpkg']+ " succeeded"
                    );
                    
                else:
                    print(self.RED + "ERROR: In json file targetpkg is not a string" + self.NC)
                    if isinstance(anArchReleaseCandidate.robotpkg_mng_vars['targetpkg'],list) :
                        print(self.RED + "use targetpkgs instead" + self.NC)
                        self.notify_wrong("Robotpkg helpers","Error in JSON file - Use targetpkgs instead");
            else:
                # If we have a list of package to compile
                if 'targetpkgs' in self.arch_release_candidate.robotpkg_mng_vars:
                    for pkg_name in self.arch_release_candidate.robotpkg_mng_vars['targetpkgs']:
                        arpgtestrc.compile_package(pkg_name)

        else:
            self.notify_wrong("Error while processing","Wrong handling of packages")


if __name__ == "__main__":
    arpkgh_build_arch_rc = RpkghBuildArchReleaseCandidate()
