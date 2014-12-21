Cloudefigo
==========
Cloudefigo is an open source tool providing an automated approach to secure IaaS instances. This version focused on Amazon Web Services EC2 instances, but the idea can be implemented in other services and cloud providers.
## Workflows
---------------
### Launch Secure Instance
1. A management user executes a secure instance launch request.
2. A new dynamic [IAM role](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html) (new approach by Cloudefigo) is created with minimal permissions to perform the steps in this flow.
3. The new instance created in the remediation security group, with the new dynamic IAM role. This means that the instance have permissions to perform avtivities, exactly as group of users would have permissions if assigned.
4. When the instance starts first time, it performs a software upgrade and installs pre-requisites.
5. Following successful installation, the instance attaches a new volume and performs full disk encryption in a secure manner. The encryption keys can be stored on HSM, but S3 can also be used for that, by creating a dynamic policy (new approach by Cloudefigo) for the specific instance. This process executed by enforcing pre-configured [Chef](https://www.getchef.com/chef/) policy on the instance.
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

### Cloning the Code
To get a local copy of the current code, clone it using git:
```
$ git clone https://github.com/valtmanir/Cloudefigo.git Cloudefigo
$ cd Cloudefigo
```
### Setting the IaaS Environment
1. Create a new instance of the latest Ubuntu and assign an [Elastic IP](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html) to it. Then, install Nessus on this instance.
2. Get [Chef for AWS](https://www.getchef.com/solutions/aws/) and assign an Elastic IP to it as well.
3. Create a new user and group for Cloudefigo management operations. Then, add the following policy to the group:
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Stmt1413548658000",
      "Effect": "Allow",
      "Action": [
        "ec2:ModifyInstanceAttribute",
        "ec2:RunInstances",
        "ec2:CreateTags"
      ],
      "Resource": [
        "*"
      ]
    },
    {
      "Sid": "Stmt1413627168000",
      "Effect": "Allow",
      "Action": [
        "iam:CreateRole",
        "iam:GetRole",
        "iam:ListRoles",
        "iam:PutRolePolicy",
        "iam:CreateInstanceProfile",
        "iam:GetInstanceProfile",
        "iam:AddRoleToInstanceProfile",
        "iam:PassRole"
      ],
      "Resource": [
        "*"
      ]
    },
{
      "Sid": "Stmt1417412719000",
      "Effect": "Allow",
      "Action": [
        "cloudtrail:DescribeTrails"
      ],
      "Resource": [
        "*"
      ]
    },
    {
      "Sid": "Stmt1417412836000",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::cloud-log-trial",
        "arn:aws:s3:::cloud-log-trial/*"
      ]
    }
  ]
}
```
Note that resource names may be different between environments.
4. [Generate API keys](http://docs.aws.amazon.com/general/latest/gr/getting-aws-sec-creds.html) for this user and store them for the coming steps.

### Setting the Management Computer Environment
1. Download 
2. Install [Python 2.7](https://www.python.org/download/releases/2.7/).
3. [Amazon Web Services CLI](http://aws.amazon.com/cli/) needed to manage the credentials of the management user only. Install the AWS CLI and set the credentials using the following command:
```
$ aws configure
AWS Access Key ID [None]: (your access key id)
AWS Secret Access Key [None]: (your secret access key)
Default region name [None]: 
Default output format [None]:
```
4. In order to install Pychef, the following dependencies should be installed. The first is [Python-pip](https://pypi.python.org/pypi/pip). 
5. When pip installed, it is easy to install Wheel by running the following command line:
```
pip install wheel
```
6. Then install PyChef using Wheel by running (this example runs on linux):
```
wget https://pypi.python.org/packages/2.7/P/PyChef/PyChef-0.2.3-py27-none-any.whl
wheel install PyChef-0.2.3-py27-none-any.whl
```

### Setting the Cloudefigo Parameters
#### Common Configuration File
Cloudefigo contains several parameters required in order to operate correctly. All of the parameters located in the file ```init.config```. The folowing parameters required by the cloud-init script executed on the launched instance:
1.  ```AWS.BucketPolicyPath ``` - The path to the dynamic policy should be set for the s3 bucket.
2.  ```AWS.IAMBasicPolicyPath ``` - The path to the dynamic IAM policy of the new instance during the initiation phase, i.e. before moving to production.
3.  ```AWS.IAMStrictPolicyPath ``` - The path to the dynamic IAM policy of the instance after moving to production.
4.  ```AWS.NamingPrefix ``` - Naming prefix used by Cloudefigo. It is mainly used for bucket names and dynamic policies generation.
5.  ```AWS.ProductionSecurityGroupId ``` - The security group id representing the production environment.
6.  ```AWS.ProductionSubnetId ``` - The subnet id where the instance started and promoted to production. 
7.  ```AWS.RemediationSecurityGroupId ``` - The security group id where the instance starts and performs all operations before moving to production.
8.  ```AWS.CloudInitScriptPath ``` - The path of the cloud-init script.
9.  ```AWS.EC2KeyName ``` - When starting an instance, the key name must be provided in order to allow future maintenance of the instance. 
10.  ```AWS.CanonicalUserId ``` - This setting must be defined in order to allow communications from the instances to the s3 buckets. The [Canonical User Id](http://docs.aws.amazon.com/general/latest/gr/acct-identifiers.html) can be found in by expanding the "Account Identifiers" list in the [Security Credentials](https://console.aws.amazon.com/iam/home?#security_credential) page.
11.  ```Chef.KeyFilePath ``` - The path to the PEM file generated by the Chef server.
12.  ```Chef.ValidationClientName ``` - The client name related to the key. It can be found in the Chef management under the Policy tab and Client sub-menu.
13.  ```Chef.ServerURL ``` - The URL of theChef server.
14.  ```Nessus.Protocol ``` - The protocol used to connect to the Nessus server. The default setting is https.
15.  ```Nessus.IPAddress ``` - The IP address of the Nessus server.
16.  ```Nessus.Port ``` - The port of the Nessus server. The default port id 8834.
17.  ```Nessus.Username ``` - Privileged user name in Nessus.
18.  ```Nessus.Pssword ``` - The passowrd of the user above.
19.  ```Nessus.ScanPolicyId ``` - The id of the scanning policy in Nessus.

#### Management Hardcoded Configuration
The file ```manage.py``` contains two hardcoded parameters used only by the configuration script:
1. Look for the EC2 constructor and see the region name. It can be changed according to the relevant region name.
2. The option to create a new instance contains hardcoded instance type, machine size and the instance name. 

#### Cloud-Init Script
The script in the file ```AWS/CloudConfig.config``` contains parameters set specifically for the environment, including S3 bucket to download files from and Chef's policy name.
