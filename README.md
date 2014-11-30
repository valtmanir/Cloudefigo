Cloudefigo
==========
Cloudefigo is an open source tool providing an automated approach to secure IaaS instances. This version focused on Amazon Web Services EC2 instances, but the idea can be implemented in other services and cloud providers.
## Workflows
---------------
### Launch Secure Instance
1. A management user executes a secure instance launch request.
2. A new dynamic [IAM role](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html) (new approach by Cloudefigo) is created with minimal permissions to perform the steps in this flow.
3. The new instance created in the remediation security group, with the new dynamic IAM role. This means that the instance have permissions to perform avtivities, exactly as group of users would have permissions if assigned.
4. When the instance starts first time, it performs a software upgrade and installes pre-requisites.
5. Following successfull installation, the instance attaches a new volume and performs full disk encryption in secure manner. The encryption keys can be stored on HSM, but S3 can also be used for that, by creating a dymanic policy (new approach by Cloudefigo) for the specific instance. This process executed by enforcing pre-configured [Chef](https://www.getchef.com/chef/) policy on the instance.
6. When all configuration steps completed, a vulnerability scan executed by [Nessus](http://www.tenable.com/products/nessus/select-your-operating-system).
7. If the scan results do not contain medium risks and above, then the instance moved to the production security group.
8. Since all operations done, the dynamic IAM role is minimized to allow access only to the full disk encryption keys on S3.

### Management
In certain cases, the security manager wants to know which instances are not managed, thus he needs to run the Cloudefigo management script to compare the existing EC2 instances with the list of managed instances in the Chef server.

In addition, by enabling Amazon Web Services Cloud Trail, all audits can be written to a specific bucket. This allows to perform validation of any identity misuse in the cloud. Cloudefigo contains the ability to parse the logs and present them in more user friendly view. Note that this feature is not production ready yet. 

## Getting Started
---------------
### Pre-requisites
1. Account in Amazon Web Services with administrative privileges.
2. [Python 2.7](https://www.python.org/download/releases/2.7/) installed on your computer.
3. [Amazon Web Services CLI](http://aws.amazon.com/cli/) needed to manage the credentials of the management user only.

### Getting the Code
To get a local copy of the current code, clone it using git:
```
$ git clone https://github.com/valtmanir/Cloudefigo.git Cloudefigo
$ cd Cloudefigo
```
### Setting the IaaS Environment
1. Create a new instance of the latest Ubuntu and assign an [Elastic IP](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html) to it. Then, install Nessus on this instance.
2. Get [Chef for AWS](https://www.getchef.com/solutions/aws/) and assign an Elastic IP to it as well.
3. TODO: IAM user & permissions creation

### Setting the Management Computer Environment
TODO

### Setting the Cloudefigo Parameters
TODO
