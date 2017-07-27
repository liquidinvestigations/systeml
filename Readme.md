# `systeml`: Liquid Investigations Node Management

This Readme file contains the plan for implementing this service.

`systeml` is a service that manages the dynamic configuration (and reconfiguration)
of other services. It is intended to run both at the "first boot" phase of the system startup (by creating configuration files for all services) and during runtime, allowing users to:

- reconfigure the network settings
- connect to OpenVPN servers or start an OpenVPN server
- manage the node as a WiFi hotspot or client
- view discovered nodes
- view reports about the state of the system and the services that it runs


## Configuration file management

All configuration files and scripts are stored under `templates`.
On first boot, these will be run through the Jinja template engine and stored
under `/var/lib/liquid/`.


### Variables

The variables contain the following:
- `liquid_domain`: the FQDN for this node
- shared and secret keys for OAuth
- flags that disables or enables a certain functionality

The variables can be extracted from a directory on the filesystem.


## System control

The `systeml` package will have a REST HTTP endpoint for controlling the services on the machine.

This HTTP service will only be available locally, and will exist as a system-controlling backend to the `liquid-core`
user interface.

The `liquid-core` module will proxy requests coming from the UI to the `systeml` service, after authorizing the user.


### HTTP endpoints

    GET     /
    Returns a short summary of the general state of the node, intended for some `everything is okay` green light in the UI.
    Reports system-wide issues and/or configuration errors.

    GET     /stats
    Returns (a short history of) the following:
    - uptime
    - disk usage
    - ram usage
    - cpu load

    GET     /nodes
    Returns a list of all the discovered nodes.

    GET     /nodes/whitelist
    Returns a list of the whitelisted nodes.

    PUT     /nodes/whitelist/<node-domain>
    Adds a node name to the whitelisted ones, reconfiguring and restarting the DNS+DHCP services as needed.

    DELETE  /nodes/whitelist/<node-domain>
    Removes a node from the whiltelisted ones, reconfiguring and restarting the DNS+DHCP services as needed.

    GET     /interfaces
    Gets a list of network interfaces and ip addresses for each network, through a call to `netifaces.interfaces()`.
    This will be useful when the UI has to display a drop-down of interfaces to choose from.

    GET     /router/interface
    Returns the network interface that the DNS+DHCP server runs on.

    POST    /router/interface
    Changes interface that the DNS+DHCP server runs on, reconfiguring and restarting the services as needed.

    GET     /router/vpn/client
    Returns information about the VPN client, or returns an error if it's not running.

    POST    /router/vpn/client/connect/<server-name>
    Tries to connect the node the the VPN server with the credentials already stored internally (by previous calls to `PUT /router/vpn/servers/<server-name>`).

    GET     /router/vpn/client/servers
    Lists information about stored VPN servers.

    PUT     /router/vpn/client/servers/<server-name>
    Adds information about a VPN server to the internal database.

    DELETE  /router/vpn/client/servers/<server-name>
    Deletes stored information about a given VPN server.

    GET     /router/vpn/server
    Gets information about the VPN server that's running on the node.

    POST    /router/vpn/server
    Starts or stops the VPN server that's running on the node.

    GET     /router/wifi/hotspot
    Returns info about the hotspot service.
    This will also return the network interface on which the service is running.

    POST    /router/wifi/hotspot
    Starts or stops the hotspot service. Through this endpoint you should be able to overwrite the following settings:
    - wifi country RF band
    - ssid and password
    - started or stopped

    GET     /router/wifi/client
    Returns info about the state of the wifi client.

    POST    /router/wifi/client
    Connects to/disconnects from a wifi network as a client.

    GET     /https
    Returns info about https configuration, certificates.

    POST    /https
    Overwrite https configuration and certificates (or ask the node to generate them).

    GET     /service/<service-name>
    Gets the status of a service in detail (e.g. hoover, hypothesis, matrix, liquid-core) from supervisor. Will return state (running, not running, error) and uptime.

