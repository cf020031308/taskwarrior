#!/usr/bin/python

import os
import commands

import utils


RESERVED_TAGS = set('nocolor nonag nocal next'.split())


def main():
    inputs = utils.format_inputs()
    args, cmd = inputs['args'], inputs['command']
    if cmd == 'split':
        # task <id> split <mods>
        pre, mods = args.split(cmd, 1)
        _id = int(pre.split()[1])
        mods = (
            (mods + ' ')
            .replace(' project: ', '')
            .replace(' project:', 'project:{}.')
            .strip())
        subid = commands.getoutput(
           'task _get %s.project | '
           'xargs -I{} task add %s | '
           'grep -o "[0-9]\\+"' %
           (_id, mods))
        if subid:
            print 'Created task %s.' % subid
            os.system('task %s modify depends:%s' % (_id, subid))
        else:
            print 'You can only split a task when it is a project.'
    elif cmd == 'timew':
        # task <id> timew ...
        pre, timew = args.split(cmd, 1)
        _id = int(pre.split()[1])
        tags, proj, uuid = commands.getoutput(
            'task _get %s.tags %s.project %s.uuid' % (_id, _id, _id)
        ).split(' ', 2)
        tags = [t for t in tags.split(',') if t not in RESERVED_TAGS]
        while proj:
            tags.append(proj)
            proj = proj.rpartition('.')[0]
        tags.append(uuid)
        tags = ' '.join('"%s"' % t for t in tags)
        os.system('timew %s %s' % (timew, tags))
    elif cmd == 'pomodoro':
        # task <id> pomodoro <annotation>
        pre, anno = args.split(cmd, 1)
        if anno.strip():
            _id = int(pre.split()[1])
            os.system(
                'task %(_id)s annotate "Pomodoro:%(anno)s" && '
                'task %(_id)s timew start pomodoro' % locals())
        else:
            os.system('%s timew start pomodoro' % pre)


main()
