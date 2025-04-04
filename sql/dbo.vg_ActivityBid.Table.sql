USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_ActivityBid]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_ActivityBid](
	[ActivityID] [int] NOT NULL,
	[ItemID] [int] NOT NULL,
	[Amount] [decimal](18, 2) NOT NULL,
	[Detail] [varchar](50) NOT NULL,
 CONSTRAINT [PK_vg_ActivityBid] PRIMARY KEY CLUSTERED 
(
	[ActivityID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[vg_ActivityBid] ADD  CONSTRAINT [DF_vg_ActivityBid_Amount]  DEFAULT ((0)) FOR [Amount]
GO
ALTER TABLE [dbo].[vg_ActivityBid] ADD  CONSTRAINT [DF_vg_ActivityBid_Detail]  DEFAULT ('') FOR [Detail]
GO
ALTER TABLE [dbo].[vg_ActivityBid]  WITH CHECK ADD  CONSTRAINT [FK_vg_ActivityBid_vg_ActivityBaseTable] FOREIGN KEY([ActivityID])
REFERENCES [dbo].[vg_ActivityBaseTable] ([ActivityID])
GO
ALTER TABLE [dbo].[vg_ActivityBid] CHECK CONSTRAINT [FK_vg_ActivityBid_vg_ActivityBaseTable]
GO
