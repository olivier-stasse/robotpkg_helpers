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

        # if self.json_filename!=None:
        #     if os.path.isfile(self.json_filename[0]):
        #         anArchReleaseCandidate.load_rc(self.json_filename[0])
        #     else:
        #         print('File '+self.json_filename[0]+' does not exists.')
        #         sys.exit(-1)

        # # Reading rpkg_mng_root
        # # On line command has priority
        # if not hasattr(self,'robotpkg_mnt_root'):
        #     # over file
        #     if 'robotpkg_mng_root' in anArchReleaseCandidate.robotpkg_mng_vars.keys():
        #         self.rpkgmngroot = anArchReleaseCandidate.robotpkg_mng_vars['robotpkg_mng_root']

        # # Reading ramfsmntpot
        # # On line command has priority
        # if not hasattr(self,'ramfsmntpt'):
        #     if 'ramfs_mnt_pt' in anArchReleaseCandidate.robotpkg_mng_vars.keys():
        #         self.sub_ramfsmntpt = anArchReleaseCandidate.robotpkg_mng_vars['ramfs_mnt_pt']

        # # Reading verbosity
        # # Define the debug level
        # if not hasattr(self,'verbosity'):
        #     if 'verbosity' in anArchReleaseCandidate.robotpkg_mng_vars.keys():
        #         self.verbosity = anArchReleaseCandidate.robotpkg_mng_vars['verbosity']

        # # Reading arch_dist_files
        # # On line commans has priority
        # if not hasattr(self,'arch_dist_files'):
        #     if 'arch_dist_files' in anArchReleaseCandidate.robotpkg_mng_vars.keys():
        #         self.arch_dist_files = anArchReleaseCandidate.robotpkg_mng_vars['arch_dist_files']
        #     else:
        #         print("No arch_dist_files in json file")
                
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

    def handle_options(self):
        parser = argparse.ArgumentParser(
            description='Build an integration tests from filename.')
        parser.add_argument('json_filename', metavar="json_filename",
            action="store", nargs='+',
            help='Name of the json specifying the architecture to build')

        parser.add_argument("-m", "--ramfsmntpt",
            dest="sub_ramfsmntpt", action="store",
            default="robotpkg-test-rc",nargs=1,
            help='Subdirectory in ROBOTPKG_MNG_ROOT to compress \n' +
                '(default:robotpkg-test-rc)')

        parser.add_argument("-r", "--rpkgmngroot", dest="rpkgmngroot", action="store",
                            default="/integration_tests", nargs=1,
                            help='Directory corresponding to ROBOTPKG_MNG_ROOT \n(default: /integration_tests)')

        parser.add_argument("-a", "--archdistfiles", dest='sub_arch_dist_files', action='store',
                            default='arch_disfiles',nargs=1,
                            help='Subdirectory in ROBOTPKG_MNG_ROOT where tar balls of packages are stored\n (default: archives)')

        parser.add_argument("-t", "--targetpkg", dest='targetpkg', action='store',
                            default='talos-dev',nargs=1,
                            help='Package to compile\n (default: talos-dev)')

        parser.add_argument("-v", "--verbosity", dest='verbosity', action='store',
                            default='0',nargs=1,
                            help='Level of verbosity\n (default: 0)')

        parser.parse_args(namespace=self)

if __name__ == "__main__":
    arpkgh_build_arch_rc = RpkghBuildArchReleaseCandidate()
