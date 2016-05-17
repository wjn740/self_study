create view performance_view as select 
    a.submission_id, 
    b.arch, 
    c.product, 
    d.`release`, 
    e.host, 
    f.log_url, 
    g.testsuite, 
    h.test_time,
    i.testcase,
    j.kernel_version 
    from submission a 
        join arch b 
            on a.arch_id = b.arch_id
        join product c 
            on a.product_id = c.product_id
        join `release` d 
            on a.release_id = d.release_id
        join host e
            on a.host_id = e.host_id
        join tcf_group f
            on a.submission_id = f.submission_id
        join testsuite g
            on f.testsuite_id = g.testsuite_id
        join result h
            on f.tcf_id = h.tcf_id
        join testcase i
            on i.testcase_id = h.testcase_id
        join kernel_version j
            on a.kernel_version_id = j.kernel_version_id
;
