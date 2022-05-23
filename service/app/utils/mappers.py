import json

#   Generated nested tree structure of comments and their recursive replies from a flat list
#   Experimenting this method, dont use yet.
#
from service.domain.domain import CommentData


def get_comments_tree(comments):
    parents = {}
    res = {}
    for comment in comments:
        parent_id = comment.parent_comment_id
        if parent_id is not None:
            # if not top level comment and also not nested comment level ( would have been in parents )
            if parent_id not in res:
                # some kind arbitrary deep of nested comment
                if parent_id in parents:
                    p_id = parents[parent_id]
                    while parents[p_id] != p_id:
                        p_id = parents[p_id]
                    queue = [res[p_id]]
                    while len(queue) > 0:
                        c = queue.pop()
                        if c.id == parent_id:
                            c.replies.append(CommentData(id=comment.id, project_id=comment.project_id, user_id=comment.user_id,
                                                 parent_comment_id=comment.parent_comment_id, content=comment.content, active=comment.active,
                                                 created_timestamp=comment.created_timestamp, replies=[]))
                            break
                        else:
                            for reply in c.replies:
                                queue.append(reply)
                else:
                    # direct reply of top level comment
                    parent = next(filter(lambda x:x.id == parent_id, comments))
                    res[parent.id] = CommentData(id=parent.id, project_id=parent.project_id, user_id=parent.user_id,
                                                 parent_comment_id=parent.parent_comment_id, content=parent.content, active=parent.active,
                                                 created_timestamp=parent.created_timestamp, replies=[])
            else:
                parent = res[parent_id]
                res[parent.id].replies.append(CommentData(id=comment.id, project_id=comment.project_id, user_id=comment.user_id,
                                                 parent_comment_id=comment.parent_comment_id, content=comment.content, active=comment.active,
                                                 created_timestamp=comment.created_timestamp, replies=[]))
                parents[comment.id] = parent.id
        else:
            res[comment.id] = CommentData(id=comment.id, project_id=comment.project_id, user_id=comment.user_id,
                                                 parent_comment_id=comment.parent_comment_id, content=comment.content, active=comment.active,
                                                 created_timestamp=comment.created_timestamp, replies=[])
            parents[comment.id] = comment.id
    return [x[1] for x in res.items()]
