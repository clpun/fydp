Install Java on Ubuntu

https://www.digitalocean.com/community/tutorials/how-to-install-java-on-ubuntu-with-apt-get

Then update Java

sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java7-installer

To automatically set up the Java 7 environment variables JAVA_HOME and PATH:
sudo apt-get install oracle-java7-set-default

To Run the jar program:
java -jar RandomPictures.jar
