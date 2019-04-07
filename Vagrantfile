# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|


  config.vm.provider "virtualbox" do |v|
        v.memory = 2048
        v.cpus = 2
    end

    config.vm.define "filesonline" do |machine|
        config.vm.box = "ubuntu/bionic64"

        machine.vm.network "private_network", ip: "192.168.10.55"

        machine.vm.synced_folder ".", "/opt/dev/filesonline"

        config.vm.provision "shell", path: "./vagrant/provision.sh"
    end
end
