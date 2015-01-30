Cloudefigo
==========
## Introduction
Cloudefigo is an open source tool providing an automated approach to secure IaaS instances. Currently Cloudefigo is focused focused on Amazon Web Services EC2 instances, however the idea can be implemented in other services and cloud providers.

### Who should use it?
Any company managing its main or shadow IT in the cloud may use Cloudefigo to automatically secure the infrastructure. The existing solution leverages few tools that can be free or commercial - all can be changed by simply replacing the code behind the scenes in order to integrate with company's standard tools. <br>
Although Cloudefigo written in Python, the cloud infrastructure administrators can use it without having experience with coding. However, a knowledge of system infrastructure is required in order to understand the processes the Cloudefigo performs (to be explained in this wiki).

### License
This tool is published under General Public License ([GPL](https://github.com/valtmanir/Cloudefigo/blob/master/LICENSE)).


## Workflows
### Launch Secure Instance
1. A management user executes a secure instance launch request.
2. A new dynamic [IAM role](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html) (new approach by Cloudefigo) is created with minimal permissions to perform the steps in this flow.
3. The new instance created in the remediation security group, with the new dynamic IAM role. This means that the instance has permissions to perform activities, exactly as a group of users would have permissions if assigned.
4. When the instance starts first time, it performs a software upgrade and installs pre-requisites.
5. Following successful installation, the instance attaches a new volume and performs full disk encryption in a secure manner. The encryption keys can be stored on HSM, but S3 can also be used for that, by creating a dynamic policy (new approach by Cloudefigo) for the specific instance. This process executed by enforcing pre-configured [Chef](https://www.getchef.com/chef/) policy on the instance.
6. When all configuration steps completed, a vulnerability scan executed by [Nessus](http://www.tenable.com/products/nessus/select-your-operating-system).
7. If the scan results do not contain medium risks and above, then the instance moved to the production security group.
8. Since all operations done, the dynamic IAM role is minimized to allow access only to the full disk encryption key on S3.

### Management
In certain cases, the security manager wants to know which instances are not managed, thus he needs to run the Cloudefigo management script to compare the existing EC2 instances with the list of managed instances in the Chef server.

In addition, by enabling Amazon Web Services Cloud Trail, all audits can be written to a specific bucket. This allows to perform validation of any identity misuse in the cloud. Cloudefigo contains the ability to parse the logs and store them in a relational database. By storing the data in such formant, System Incident and Event Management (SIEM) products can pull the data and correlate it in order to identify abnormal activities.

## Getting Started
### Cloning the Code
To get a local copy of the current code, clone it using git:
```
$ git clone https://github.com/valtmanir/Cloudefigo.git Cloudefigo
$ cd Cloudefigo
```
### Documentation
Please review Cloudefigo documentation on https://github.com/valtmanir/Cloudefigo/wiki