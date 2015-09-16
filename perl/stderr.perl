#!/usr/bin/perl
use IPC::Open3;
use Symbol;

my ($child_in,$child_out,$child_err);
$child_err=gensym();

my $dir = "/home/jnwang/workdir/study_dir/perl";
my @git = ('git', '--git-dir', "$dir/.git", '--work-tree', $dir);
my $file = "abs";

eval{
$pid=open3($child_in,$child_out,$child_err,'date -hking');
};
die "open3: $@\n" if $@;

waitpid($pid,0);
my $ret=$? >> 8;


#while( my $output = <READER>) {
#    print "$output";
#}
#while( my $output = <$child_out>) {
#    print "$output";
#}

if($ret) {
    die "ret = $ret";
    die "failed to git add $name";
}
#open my $text_err, '<', $child_out

#print $text_err
