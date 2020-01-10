# PNC / Indy Metadata Cleanup Utility

This utility will lookup the output artifacts for one or more builds from the PNC build system, convert them into Maven metadata paths, and issue a series of DELETE requests to a selected set of repositories or groups in the Indy repository manager.

This is sometimes necessary after a major upgrade or data migration (or when deploying new features) to cope with stale metadata. Also, at times, metadata may become stale as a result of network failures with one or more service integration points. This should help remediate the problem.

## Installation - Localhost

You can setup a virtualenv, install / upgrade `pip`, and then install the cleanup utility using the following shell script:

```bash
$ ./setup.sh
```

## Configuration

Configuration happens using an environment YAML file, which is supplied as argument #1 in the command-line execution:

```bash
$ pnc-clear-metadata /path/to/env.yml BUILD_ID1 BUILD_ID2 ...
```

At a minimum, you'll need to provide URLs for PNC and Indy:

```yaml
indy-url: http://indy.psi.redhat.com
pnc-url: http://orch.psi.redhat.com	
```

This utility can authenticate DELETE requests using an OAuth system that PNC and Indy share. To enable this, you'll need to add a `sso` section to your environment configuration:

```yaml
indy-url: http://indy.pnc.somedomain.corp
pnc-url: http://orch.pnc.somedomain.corp

sso:
  enabled: true
  url: https://keycloak.somedomain.corp
  realm: keycloak-realm-name
  grant-type: password
  client-id: my-keycloak-client-id
  client-secret: aaaabbbb-eeee-9999-0000-asdfadfadsfad
```

By default, this utility will clear metadata paths from a group called `builds-untested` (`maven:group:builds-untested`). If you want to override this, maybe so you can add more targets, you can do that with the following YAML snippet:

```yaml
indy-url: ...
pnc-url: ...

clear-stores:
  - maven:group:builds-untested
  - maven:group:static-builds
  - maven:group:my-special-builds

...
```

## Execution

Execution is pretty simple, as noted in the beginning of the Configuration section above:

```bash
$ pnc-clear-metadata /path/to/env.yml BUILD_ID1 BUILD_ID2 ...
```

You can also print the help screen using:

```bash
$ pnc-clear-metadata --help
```