def handle_registration(config):
    '''
        Handle the registration process
    '''
    # def _clear_all():
    #     delete_registered_file()
    #     delete_unregistered_file()
    #     write_to_disk(constants.machine_id_file, delete=True)

    # if config.reregister:
    #     _clear_all()

    logger.debug('Machine-id: %s', generate_machine_id(config.reregister))

    # check registration with API
    check = get_registration_status(config)

    for m in check['messages']:
        logger.debug(m)

    if check['unreachable']:
        # Run connection test and exit
        return

    if check['status']:
        # registered in API, resync files
        if config.register:
            logger.info('This host has already been registered.')
        write_registered_file()
        delete_unregistered_file()
        return

    # unregistered in API, resync files
    delete_registered_file()
    if unreg_date:
        write_unregistered_file(date=unreg_date)

    if config.register:
        # register if specified
        message, hostname, group, display_name = register(config)
        if config.display_name is None and config.group is None:
            logger.info('Successfully registered host %s', hostname)
        elif config.display_name is None:
            logger.info('Successfully registered host %s in group %s',
                        hostname, group)
        else:
            logger.info('Successfully registered host %s as %s in group %s',
                        hostname, display_name, group)
        if message:
            logger.info(message)
        return reg_check, message, hostname, group, display_name
    else:
        # print messaging and exit
        if unreg_date:
            # registered and then unregistered
            logger.info('This machine has been unregistered. '
                        'Use --register if you would like to '
                        're-register this machine.')
        else:
            # not yet registered
            logger.info('This machine has not yet been registered.'
                        'Use --register to register this machine.')
        return


def register(config):
    """
    Do registration using basic auth
    """
    username = config.username
    password = config.password
    authmethod = config.authmethod
    auto_config = config.auto_config
    if not username and not password and not auto_config and authmethod == 'BASIC':
        logger.debug('Username and password must be defined in configuration file with BASIC authentication method.')
        return False
    pconn = get_connection(config)
    return pconn.register()


def get_registration_status(config):
    return registration_check(get_connection(config))


def handle_unregistration(config):
    """
        returns (bool): True success, False failure
    """
    pconn = get_connection(config)
    return pconn.unregister()